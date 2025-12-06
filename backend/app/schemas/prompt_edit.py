"""Pydantic schemas for prompt-based code editing"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class RepoContext(BaseModel):
    """Repository context for code editing"""

    repo_path: Optional[str] = Field(None, description="Root path of the repository")
    files: Optional[List[str]] = Field(
        None, description="List of relevant file paths"
    )
    file_contents: Optional[Dict[str, str]] = Field(
        None, description="Map of file paths to their contents"
    )
    language: Optional[str] = Field(None, description="Primary programming language")
    framework: Optional[str] = Field(None, description="Framework or library used")
    additional_context: Optional[Dict[str, Any]] = Field(
        None, description="Additional context information"
    )


class PromptSubmitRequest(BaseModel):
    """Request schema for submitting a prompt"""

    prompt: str = Field(..., description="User prompt describing desired changes")
    repo_context: Optional[RepoContext] = Field(
        None, description="Repository context"
    )
    target_files: Optional[List[str]] = Field(
        None, description="Specific files to target for editing"
    )
    dry_run: bool = Field(
        True, description="Whether to only plan without applying changes"
    )
    llm_provider: str = Field(
        "openai", description="LLM provider to use (openai, anthropic, local)"
    )
    llm_model: Optional[str] = Field(None, description="Specific model to use")


class EditPlan(BaseModel):
    """Single edit plan for a file"""

    file_path: str = Field(..., description="Path to the file to edit")
    edit_type: str = Field(
        ..., description="Type of edit (create, modify, delete, rename)"
    )
    description: str = Field(..., description="Description of the edit")
    original_content: Optional[str] = Field(None, description="Original file content")
    modified_content: Optional[str] = Field(None, description="Modified file content")
    line_range: Optional[tuple[int, int]] = Field(
        None, description="Line range affected by edit"
    )


class PromptSubmitResponse(BaseModel):
    """Response schema for prompt submission"""

    session_id: str = Field(..., description="Unique session identifier")
    status: str = Field(..., description="Session status")
    message: str = Field(..., description="Status message")
    edit_plans: List[EditPlan] = Field(
        default_factory=list, description="List of generated edit plans"
    )
    created_at: str = Field(..., description="Session creation timestamp")


class DiffPreview(BaseModel):
    """Diff preview for a single file"""

    file_path: str = Field(..., description="Path to the file")
    diff: str = Field(..., description="Unified diff output")
    additions: int = Field(0, description="Number of lines added")
    deletions: int = Field(0, description="Number of lines deleted")
    edit_type: str = Field(..., description="Type of edit")


class DiffPreviewResponse(BaseModel):
    """Response schema for diff preview"""

    session_id: str = Field(..., description="Session identifier")
    diffs: List[DiffPreview] = Field(..., description="List of diff previews")
    total_files: int = Field(..., description="Total number of files affected")
    total_additions: int = Field(..., description="Total lines added")
    total_deletions: int = Field(..., description="Total lines deleted")


class ApplyEditRequest(BaseModel):
    """Request schema for applying edits"""

    session_id: str = Field(..., description="Session identifier")
    file_paths: Optional[List[str]] = Field(
        None, description="Specific files to apply (None = all)"
    )
    skip_validation: bool = Field(
        False, description="Skip validation before applying"
    )
    auto_format: bool = Field(True, description="Automatically format after applying")


class ApplyEditResponse(BaseModel):
    """Response schema for applied edits"""

    session_id: str = Field(..., description="Session identifier")
    applied_files: List[str] = Field(..., description="List of applied files")
    failed_files: List[str] = Field(
        default_factory=list, description="List of files that failed"
    )
    status: str = Field(..., description="Overall status")
    message: str = Field(..., description="Status message")
    errors: Optional[List[Dict[str, str]]] = Field(
        None, description="List of errors if any"
    )


class FormatRequest(BaseModel):
    """Request schema for formatting code"""

    session_id: str = Field(..., description="Session identifier")
    file_paths: Optional[List[str]] = Field(
        None, description="Specific files to format (None = all)"
    )
    formatters: Optional[List[str]] = Field(
        None, description="Specific formatters to use (black, ruff, prettier)"
    )


class FormatResult(BaseModel):
    """Result of formatting a single file"""

    file_path: str = Field(..., description="Path to the file")
    formatter: str = Field(..., description="Formatter used")
    status: str = Field(..., description="Format status (success, failed, skipped)")
    message: Optional[str] = Field(None, description="Status message or error")
    formatted_content: Optional[str] = Field(
        None, description="Formatted content when changes were made"
    )
    changes_made: bool = Field(False, description="Whether changes were made")


class FormatResponse(BaseModel):
    """Response schema for formatting"""

    session_id: str = Field(..., description="Session identifier")
    results: List[FormatResult] = Field(..., description="Formatting results")
    total_formatted: int = Field(..., description="Number of files formatted")
    total_changed: int = Field(..., description="Number of files changed")


class ValidationRequest(BaseModel):
    """Request schema for validating edits"""

    session_id: str = Field(..., description="Session identifier")
    validation_types: List[str] = Field(
        default=["syntax", "lint", "type"],
        description="Types of validation to perform",
    )


class ValidationResult(BaseModel):
    """Result of a single validation check"""

    validation_type: str = Field(..., description="Type of validation")
    status: str = Field(..., description="Validation status (pass, fail, warning)")
    file_path: Optional[str] = Field(None, description="File path if applicable")
    message: str = Field(..., description="Validation message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional details")


class ValidationResponse(BaseModel):
    """Response schema for validation"""

    session_id: str = Field(..., description="Session identifier")
    results: List[ValidationResult] = Field(..., description="Validation results")
    overall_status: str = Field(..., description="Overall validation status")
    passed: int = Field(..., description="Number of checks passed")
    failed: int = Field(..., description="Number of checks failed")
    warnings: int = Field(..., description="Number of warnings")


class TestRunRequest(BaseModel):
    """Request schema for running tests"""

    session_id: str = Field(..., description="Session identifier")
    test_command: Optional[str] = Field(None, description="Custom test command")
    test_paths: Optional[List[str]] = Field(
        None, description="Specific test paths to run"
    )
    coverage: bool = Field(False, description="Generate coverage report")


class TestRunResponse(BaseModel):
    """Response schema for test runs"""

    session_id: str = Field(..., description="Session identifier")
    status: str = Field(..., description="Test run status")
    passed: int = Field(0, description="Number of tests passed")
    failed: int = Field(0, description="Number of tests failed")
    skipped: int = Field(0, description="Number of tests skipped")
    duration: float = Field(0.0, description="Test duration in seconds")
    output: str = Field(..., description="Test output")
    coverage_percent: Optional[float] = Field(None, description="Code coverage %")


class SessionStatusResponse(BaseModel):
    """Response schema for session status"""

    session_id: str = Field(..., description="Session identifier")
    status: str = Field(..., description="Current status")
    prompt: str = Field(..., description="Original prompt")
    edit_count: int = Field(..., description="Number of edits planned")
    applied_count: int = Field(..., description="Number of edits applied")
    validated: bool = Field(..., description="Whether edits have been validated")
    formatted: bool = Field(..., description="Whether edits have been formatted")
    tests_run: bool = Field(..., description="Whether tests have been run")
    created_at: str = Field(..., description="Session creation timestamp")
    updated_at: str = Field(..., description="Last update timestamp")
