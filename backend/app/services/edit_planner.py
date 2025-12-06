"""Service for planning code edits based on user prompts"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import uuid4

from sqlalchemy.orm import Session

from app.models.prompt_edit import CodeEdit, EditSession
from app.schemas.prompt_edit import EditPlan, RepoContext
from app.services.llm_provider import LLMProvider, LLMProviderFactory


class EditPlannerService:
    """Service for generating code edit plans from prompts"""

    def __init__(self, db: Session, repo_root: Optional[str] = None):
        self.db = db
        self.repo_root = Path(repo_root or os.getenv("REPO_ROOT", "/home/engine/project"))

    def _build_system_prompt(self) -> str:
        """Build system prompt for the LLM"""
        return """You are an expert software engineer helping to plan code changes.
Your task is to analyze a user's request and generate a detailed plan for code modifications.

You should:
1. Understand the user's intent clearly
2. Identify which files need to be modified, created, or deleted
3. Provide clear descriptions of what changes are needed
4. Generate the complete modified content for each file
5. Consider best practices, code quality, and maintainability

Respond with a JSON object containing:
{
    "edits": [
        {
            "file_path": "path/to/file.py",
            "edit_type": "modify|create|delete|rename",
            "description": "Clear description of changes",
            "modified_content": "Complete file content after changes"
        }
    ],
    "summary": "Overall summary of changes"
}

For modifications, provide the complete new file content.
For new files, provide the full content to create.
For deletions, set modified_content to null.
"""

    def _build_user_prompt(
        self, prompt: str, repo_context: Optional[RepoContext], target_files: List[str]
    ) -> str:
        """Build the user prompt with context"""
        parts = [f"User Request: {prompt}\n"]

        if repo_context:
            if repo_context.repo_path:
                parts.append(f"Repository Path: {repo_context.repo_path}")

            if repo_context.language:
                parts.append(f"Primary Language: {repo_context.language}")

            if repo_context.framework:
                parts.append(f"Framework: {repo_context.framework}")

            if repo_context.files:
                parts.append(f"\nRelevant Files ({len(repo_context.files)}):")
                for file_path in repo_context.files[:10]:
                    parts.append(f"  - {file_path}")

            if repo_context.file_contents:
                parts.append("\nFile Contents:")
                for file_path, content in list(repo_context.file_contents.items())[:5]:
                    parts.append(f"\n--- {file_path} ---")
                    lines = content.split("\n")
                    if len(lines) > 50:
                        parts.append("\n".join(lines[:25]))
                        parts.append(f"\n... ({len(lines) - 50} lines omitted) ...")
                        parts.append("\n".join(lines[-25:]))
                    else:
                        parts.append(content)

        if target_files:
            parts.append(f"\nTarget Files: {', '.join(target_files)}")

        return "\n".join(parts)

    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM response into structured data"""
        try:
            # Try to parse as JSON
            if response.strip().startswith("{"):
                return json.loads(response)
        except json.JSONDecodeError:
            pass

        # Try to extract JSON from markdown code blocks
        json_match = re.search(r"```json\s*\n(.*?)\n```", response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass

        # Fallback: return a simple structure
        return {
            "edits": [],
            "summary": response[:500],
            "parse_error": "Could not parse structured response",
        }

    async def create_edit_plan(
        self,
        prompt: str,
        repo_context: Optional[RepoContext],
        target_files: Optional[List[str]],
        llm_provider_name: str,
        llm_model: Optional[str],
        dry_run: bool,
    ) -> tuple[str, List[EditPlan]]:
        """
        Create edit plan from user prompt

        Args:
            prompt: User prompt describing desired changes
            repo_context: Repository context information
            target_files: Specific files to target
            llm_provider_name: Name of LLM provider to use
            llm_model: Specific model to use
            dry_run: Whether this is a dry run

        Returns:
            Tuple of (session_id, list of edit plans)
        """
        # Create session
        session_id = str(uuid4())

        # Get LLM provider
        llm_provider = LLMProviderFactory.create(
            llm_provider_name, model=llm_model or self._get_default_model(llm_provider_name)
        )

        if not llm_provider.is_available():
            llm_provider = LLMProviderFactory.create("mock")

        # Build prompts
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(
            prompt, repo_context, target_files or []
        )

        # Generate edit plan
        try:
            if llm_provider_name != "mock":
                response = llm_provider.generate_completion(
                    user_prompt,
                    system_prompt=system_prompt,
                    temperature=0.3,
                    max_tokens=4000,
                )
                parsed = self._parse_llm_response(response)
            else:
                parsed = self._generate_mock_plan(prompt, target_files)
        except Exception as e:
            parsed = {
                "edits": [],
                "summary": f"Error generating plan: {str(e)}",
                "error": str(e),
            }

        # Create session record
        edit_session = EditSession(
            session_id=session_id,
            user_prompt=prompt,
            repo_context=repo_context.model_dump() if repo_context else None,
            status="plan_generated",
            llm_provider=llm_provider_name,
            llm_model=llm_model,
            dry_run=dry_run,
        )
        self.db.add(edit_session)

        # Create edit records
        edit_plans = []
        for edit_data in parsed.get("edits", []):
            code_edit = CodeEdit(
                session_id=session_id,
                file_path=edit_data.get("file_path", "unknown"),
                edit_type=edit_data.get("edit_type", "modify"),
                description=edit_data.get("description", ""),
                original_content=edit_data.get("original_content"),
                modified_content=edit_data.get("modified_content"),
            )
            self.db.add(code_edit)

            edit_plans.append(
                EditPlan(
                    file_path=code_edit.file_path,
                    edit_type=code_edit.edit_type,
                    description=code_edit.description,
                    original_content=code_edit.original_content,
                    modified_content=code_edit.modified_content,
                )
            )

        self.db.commit()

        return session_id, edit_plans

    def _get_default_model(self, provider_name: str) -> str:
        """Get default model for provider"""
        defaults = {
            "openai": "gpt-4",
            "anthropic": "claude-3-sonnet-20240229",
            "mock": "mock-model",
        }
        return defaults.get(provider_name, "default")

    def _generate_mock_plan(
        self, prompt: str, target_files: Optional[List[str]]
    ) -> Dict[str, Any]:
        """Generate a mock edit plan for testing"""
        edits = []

        if target_files:
            for file_path in target_files[:3]:
                edits.append(
                    {
                        "file_path": file_path,
                        "edit_type": "modify",
                        "description": f"Mock modification for {file_path} based on: {prompt[:100]}",
                        "modified_content": f"# Modified content for {file_path}\n# Based on prompt: {prompt[:50]}\n\npass\n",
                    }
                )
        else:
            edits.append(
                {
                    "file_path": "example.py",
                    "edit_type": "create",
                    "description": f"Mock file creation based on: {prompt[:100]}",
                    "modified_content": f'"""Mock file created by prompt edit engine"""\n\n# Prompt: {prompt[:100]}\n\ndef example_function():\n    """Example function"""\n    pass\n',
                }
            )

        return {
            "edits": edits,
            "summary": f"Mock edit plan: {len(edits)} file(s) to be modified based on prompt.",
        }

    def get_edit_plans(self, session_id: str) -> List[EditPlan]:
        """Get all edit plans for a session"""
        edits = self.db.query(CodeEdit).filter_by(session_id=session_id).all()

        return [
            EditPlan(
                file_path=edit.file_path,
                edit_type=edit.edit_type,
                description=edit.description,
                original_content=edit.original_content,
                modified_content=edit.modified_content,
            )
            for edit in edits
        ]

    def get_session(self, session_id: str) -> Optional[EditSession]:
        """Get edit session by ID"""
        return (
            self.db.query(EditSession).filter_by(session_id=session_id).first()
        )

    def update_session_status(self, session_id: str, status: str):
        """Update session status"""
        session = self.get_session(session_id)
        if session:
            session.status = status
            self.db.commit()
