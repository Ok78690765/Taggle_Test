"""REST API endpoints for prompt-based code editing"""

import os
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.prompt_edit import CodeEdit, EditSession, EditValidation
from app.schemas.prompt_edit import (
    ApplyEditRequest,
    ApplyEditResponse,
    DiffPreview,
    DiffPreviewResponse,
    FormatRequest,
    FormatResponse,
    PromptSubmitRequest,
    PromptSubmitResponse,
    SessionStatusResponse,
    TestRunRequest,
    TestRunResponse,
    ValidationRequest,
    ValidationResponse,
)
from app.services.edit_planner import EditPlannerService
from app.services.formatting_service import FormattingService
from app.services.test_runner import TestRunnerService
from app.services.validation_service import ValidationService
from app.utils.diff_utils import count_diff_changes, generate_unified_diff

router = APIRouter(prefix="/api/prompt", tags=["Prompt Edit"])


@router.post("/submit", response_model=PromptSubmitResponse)
async def submit_prompt(
    request: PromptSubmitRequest,
    db: Session = Depends(get_db),
):
    """
    Submit a prompt to generate code edit plans

    This endpoint takes a user prompt along with repository context and
    generates a detailed plan for code modifications using an LLM.

    Args:
        request: Prompt submission request containing prompt, context, and options

    Returns:
        PromptSubmitResponse with session ID and edit plans
    """
    planner = EditPlannerService(db)

    session_id, edit_plans = await planner.create_edit_plan(
        prompt=request.prompt,
        repo_context=request.repo_context,
        target_files=request.target_files,
        llm_provider_name=request.llm_provider,
        llm_model=request.llm_model,
        dry_run=request.dry_run,
    )

    session = planner.get_session(session_id)

    return PromptSubmitResponse(
        session_id=session_id,
        status=session.status,
        message=f"Edit plan generated successfully with {len(edit_plans)} file(s)",
        edit_plans=edit_plans,
        created_at=session.created_at.isoformat(),
    )


@router.get("/{session_id}/preview", response_model=DiffPreviewResponse)
async def preview_diffs(
    session_id: str,
    db: Session = Depends(get_db),
):
    """
    Preview diffs for a session

    Generate unified diffs for all planned edits in the session.
    This allows reviewing changes before applying them.

    Args:
        session_id: Session identifier

    Returns:
        DiffPreviewResponse with unified diffs for each file
    """
    session = db.query(EditSession).filter_by(session_id=session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    edits = db.query(CodeEdit).filter_by(session_id=session_id).all()

    diffs = []
    total_additions = 0
    total_deletions = 0

    for edit in edits:
        if edit.edit_type == "delete":
            diff = f"File will be deleted: {edit.file_path}"
            additions, deletions = 0, len(edit.original_content.splitlines() if edit.original_content else [])
        elif edit.edit_type == "create":
            diff = f"File will be created: {edit.file_path}\n\n{edit.modified_content or ''}"
            additions, deletions = len(edit.modified_content.splitlines() if edit.modified_content else []), 0
        else:
            original = edit.original_content or ""
            modified = edit.modified_content or ""
            diff = generate_unified_diff(original, modified, edit.file_path)
            additions, deletions = count_diff_changes(diff)

        total_additions += additions
        total_deletions += deletions

        diffs.append(
            DiffPreview(
                file_path=edit.file_path,
                diff=diff,
                additions=additions,
                deletions=deletions,
                edit_type=edit.edit_type,
            )
        )

    return DiffPreviewResponse(
        session_id=session_id,
        diffs=diffs,
        total_files=len(diffs),
        total_additions=total_additions,
        total_deletions=total_deletions,
    )


@router.post("/{session_id}/apply", response_model=ApplyEditResponse)
async def apply_edits(
    session_id: str,
    request: ApplyEditRequest,
    db: Session = Depends(get_db),
):
    """
    Apply the planned edits to actual files

    This endpoint writes the planned changes to the filesystem.
    By default, it validates and formats the changes before applying.

    Args:
        session_id: Session identifier
        request: Apply edit request with options

    Returns:
        ApplyEditResponse with results of applying edits
    """
    session = db.query(EditSession).filter_by(session_id=session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if not session.dry_run and session.status != "plan_generated":
        raise HTTPException(
            status_code=400, detail="Session is not in a valid state for applying edits"
        )

    edits = db.query(CodeEdit).filter_by(session_id=session_id).all()

    if request.file_paths:
        edits = [e for e in edits if e.file_path in request.file_paths]

    applied_files = []
    failed_files = []
    errors = []

    repo_root = os.getenv("REPO_ROOT", "/home/engine/project")

    for edit in edits:
        try:
            file_full_path = os.path.join(repo_root, edit.file_path)

            if edit.edit_type == "delete":
                if os.path.exists(file_full_path):
                    os.remove(file_full_path)
                    edit.applied = True
                    applied_files.append(edit.file_path)
            elif edit.edit_type in ["create", "modify"]:
                if not request.skip_validation:
                    validator = ValidationService()
                    result = validator.validate_syntax(edit.file_path, edit.modified_content or "")
                    if result.status == "fail":
                        errors.append(
                            {
                                "file": edit.file_path,
                                "error": f"Syntax validation failed: {result.message}",
                            }
                        )
                        failed_files.append(edit.file_path)
                        continue

                os.makedirs(os.path.dirname(file_full_path), exist_ok=True)

                with open(file_full_path, "w") as f:
                    f.write(edit.modified_content or "")

                edit.applied = True
                applied_files.append(edit.file_path)

        except Exception as e:
            failed_files.append(edit.file_path)
            errors.append({"file": edit.file_path, "error": str(e)})

    db.commit()

    session.status = "applied" if not failed_files else "partially_applied"
    db.commit()

    if request.auto_format and applied_files:
        format_service = FormattingService()
        for file_path in applied_files:
            file_full_path = os.path.join(repo_root, file_path)
            if os.path.exists(file_full_path):
                with open(file_full_path, "r") as f:
                    content = f.read()
                results = format_service.format_file(file_path, content)
                for result in results:
                    if result.changes_made and result.formatted_content:
                        with open(file_full_path, "w") as f:
                            f.write(result.formatted_content)

    return ApplyEditResponse(
        session_id=session_id,
        applied_files=applied_files,
        failed_files=failed_files,
        status="success" if not failed_files else "partial_success",
        message=f"Applied {len(applied_files)} file(s), {len(failed_files)} failed",
        errors=errors if errors else None,
    )


@router.post("/{session_id}/format", response_model=FormatResponse)
async def format_files(
    session_id: str,
    request: FormatRequest,
    db: Session = Depends(get_db),
):
    """
    Format files in the session using appropriate formatters

    Runs formatters like Black, Ruff, or Prettier on the edited files
    to ensure Google-level code quality.

    Args:
        session_id: Session identifier
        request: Format request with options

    Returns:
        FormatResponse with formatting results
    """
    session = db.query(EditSession).filter_by(session_id=session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    edits = db.query(CodeEdit).filter_by(session_id=session_id).all()

    if request.file_paths:
        edits = [e for e in edits if e.file_path in request.file_paths]

    format_service = FormattingService()
    all_results = []
    total_formatted = 0
    total_changed = 0

    for edit in edits:
        if edit.modified_content:
            results = format_service.format_file(
                edit.file_path, edit.modified_content, request.formatters
            )
            all_results.extend(results)

            for result in results:
                if result.status == "success":
                    total_formatted += 1
                    if result.changes_made:
                        total_changed += 1
                        if result.formatted_content:
                            edit.modified_content = result.formatted_content
                            edit.formatted = True

    db.commit()

    session.formatting_status = "completed"
    db.commit()

    return FormatResponse(
        session_id=session_id,
        results=all_results,
        total_formatted=total_formatted,
        total_changed=total_changed,
    )


@router.post("/{session_id}/validate", response_model=ValidationResponse)
async def validate_edits(
    session_id: str,
    request: ValidationRequest,
    db: Session = Depends(get_db),
):
    """
    Validate planned edits

    Run various validation checks (syntax, lint, type) on the planned edits
    before applying them.

    Args:
        session_id: Session identifier
        request: Validation request with validation types

    Returns:
        ValidationResponse with validation results
    """
    session = db.query(EditSession).filter_by(session_id=session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    edits = db.query(CodeEdit).filter_by(session_id=session_id).all()

    validator = ValidationService()
    all_results = []
    passed = failed = warnings = 0

    for edit in edits:
        if edit.modified_content:
            if "syntax" in request.validation_types:
                result = validator.validate_syntax(edit.file_path, edit.modified_content)
                all_results.append(result)
                if result.status == "pass":
                    passed += 1
                elif result.status == "fail":
                    failed += 1
                else:
                    warnings += 1

            if "lint" in request.validation_types:
                result = validator.validate_lint(edit.file_path, edit.modified_content)
                all_results.append(result)
                if result.status == "pass":
                    passed += 1
                elif result.status == "fail":
                    failed += 1
                else:
                    warnings += 1

            if "type" in request.validation_types:
                result = validator.validate_type_check(edit.file_path, edit.modified_content)
                all_results.append(result)
                if result.status == "pass":
                    passed += 1
                elif result.status == "fail":
                    failed += 1
                else:
                    warnings += 1

            edit.validated = True

    for result in all_results:
        validation_record = EditValidation(
            session_id=session_id,
            validation_type=result.validation_type,
            status=result.status,
            message=result.message,
            details=result.details,
        )
        db.add(validation_record)

    db.commit()

    overall_status = "passed" if failed == 0 else "failed"
    session.validation_status = overall_status
    db.commit()

    return ValidationResponse(
        session_id=session_id,
        results=all_results,
        overall_status=overall_status,
        passed=passed,
        failed=failed,
        warnings=warnings,
    )


@router.post("/{session_id}/test", response_model=TestRunResponse)
async def run_tests(
    session_id: str,
    request: TestRunRequest,
    db: Session = Depends(get_db),
):
    """
    Run tests after applying edits

    Execute the test suite to ensure the changes don't break existing functionality.

    Args:
        session_id: Session identifier
        request: Test run request with options

    Returns:
        TestRunResponse with test results
    """
    session = db.query(EditSession).filter_by(session_id=session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    test_runner = TestRunnerService()

    response = test_runner.run_tests(
        session_id=session_id,
        test_command=request.test_command,
        test_paths=request.test_paths,
        coverage=request.coverage,
    )

    session.test_status = response.status
    db.commit()

    return response


@router.get("/{session_id}/status", response_model=SessionStatusResponse)
async def get_session_status(
    session_id: str,
    db: Session = Depends(get_db),
):
    """
    Get the status of an edit session

    Retrieve the current state of an edit session including
    progress on edits, validation, formatting, and testing.

    Args:
        session_id: Session identifier

    Returns:
        SessionStatusResponse with current session status
    """
    session = db.query(EditSession).filter_by(session_id=session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    edits = db.query(CodeEdit).filter_by(session_id=session_id).all()

    applied_count = sum(1 for e in edits if e.applied)

    return SessionStatusResponse(
        session_id=session_id,
        status=session.status,
        prompt=session.user_prompt,
        edit_count=len(edits),
        applied_count=applied_count,
        validated=session.validation_status != "pending",
        formatted=session.formatting_status != "pending",
        tests_run=session.test_status != "pending",
        created_at=session.created_at.isoformat(),
        updated_at=session.updated_at.isoformat(),
    )
