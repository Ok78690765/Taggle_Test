"""Service for formatting code using various tools"""

import os
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from app.schemas.prompt_edit import FormatResult


class FormattingService:
    """Service for formatting code files"""

    def __init__(self):
        self.formatters = {
            "python": ["black", "ruff"],
            "javascript": ["prettier"],
            "typescript": ["prettier"],
            "json": ["prettier"],
            "css": ["prettier"],
            "html": ["prettier"],
        }

    def format_file(
        self, file_path: str, content: str, formatters: Optional[List[str]] = None
    ) -> List[FormatResult]:
        """
        Format a file using appropriate formatters

        Args:
            file_path: Path to the file
            content: File content to format
            formatters: Specific formatters to use (None = auto-detect)

        Returns:
            List of format results
        """
        results = []
        language = self._detect_language(file_path)

        if formatters is None:
            formatters = self.formatters.get(language, [])

        formatted_content = content

        for formatter in formatters:
            result = self._apply_formatter(
                formatter, file_path, formatted_content, language
            )
            results.append(result)

            if (
                result.status == "success"
                and result.changes_made
                and result.formatted_content is not None
            ):
                formatted_content = result.formatted_content

        return results

    def format_files(
        self, files: Dict[str, str], formatters: Optional[List[str]] = None
    ) -> Dict[str, List[FormatResult]]:
        """
        Format multiple files

        Args:
            files: Dictionary mapping file paths to contents
            formatters: Specific formatters to use

        Returns:
            Dictionary mapping file paths to format results
        """
        results = {}

        for file_path, content in files.items():
            results[file_path] = self.format_file(file_path, content, formatters)

        return results

    def _detect_language(self, file_path: str) -> str:
        """Detect language from file extension"""
        ext = Path(file_path).suffix.lstrip(".")
        language_map = {
            "py": "python",
            "js": "javascript",
            "jsx": "javascript",
            "ts": "typescript",
            "tsx": "typescript",
            "json": "json",
            "css": "css",
            "html": "html",
            "htm": "html",
        }
        return language_map.get(ext, "unknown")

    def _apply_formatter(
        self, formatter: str, file_path: str, content: str, language: str
    ) -> FormatResult:
        """Apply a specific formatter"""
        if formatter == "black":
            return self._format_with_black(file_path, content)
        elif formatter == "ruff":
            return self._format_with_ruff(file_path, content)
        elif formatter == "prettier":
            return self._format_with_prettier(file_path, content)
        else:
            return FormatResult(
                file_path=file_path,
                formatter=formatter,
                status="skipped",
                message=f"Unknown formatter: {formatter}",
                changes_made=False,
            )

    def _format_with_black(self, file_path: str, content: str) -> FormatResult:
        """Format Python code with Black"""
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".py", delete=False
            ) as tmp:
                tmp.write(content)
                tmp_path = tmp.name

            try:
                result = subprocess.run(
                    ["black", "--quiet", "--line-length", "88", tmp_path],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )

                with open(tmp_path, "r") as f:
                    formatted_content = f.read()

                changes_made = formatted_content != content

                return FormatResult(
                    file_path=file_path,
                    formatter="black",
                    status="success" if result.returncode == 0 else "failed",
                    message=result.stderr if result.stderr else None,
                    formatted_content=formatted_content if changes_made else None,
                    changes_made=changes_made,
                )
            finally:
                os.unlink(tmp_path)

        except FileNotFoundError:
            return FormatResult(
                file_path=file_path,
                formatter="black",
                status="skipped",
                message="Black not installed",
                changes_made=False,
            )
        except Exception as e:
            return FormatResult(
                file_path=file_path,
                formatter="black",
                status="failed",
                message=str(e),
                changes_made=False,
            )

    def _format_with_ruff(self, file_path: str, content: str) -> FormatResult:
        """Format Python code with Ruff"""
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".py", delete=False
            ) as tmp:
                tmp.write(content)
                tmp_path = tmp.name

            try:
                result = subprocess.run(
                    ["ruff", "check", "--fix", tmp_path],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )

                with open(tmp_path, "r") as f:
                    formatted_content = f.read()

                changes_made = formatted_content != content

                return FormatResult(
                    file_path=file_path,
                    formatter="ruff",
                    status="success" if result.returncode == 0 else "failed",
                    message=result.stderr if result.stderr else None,
                    formatted_content=formatted_content if changes_made else None,
                    changes_made=changes_made,
                )
            finally:
                os.unlink(tmp_path)

        except FileNotFoundError:
            return FormatResult(
                file_path=file_path,
                formatter="ruff",
                status="skipped",
                message="Ruff not installed",
                changes_made=False,
            )
        except Exception as e:
            return FormatResult(
                file_path=file_path,
                formatter="ruff",
                status="failed",
                message=str(e),
                changes_made=False,
            )

    def _format_with_prettier(self, file_path: str, content: str) -> FormatResult:
        """Format code with Prettier"""
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=Path(file_path).suffix, delete=False
            ) as tmp:
                tmp.write(content)
                tmp_path = tmp.name

            try:
                result = subprocess.run(
                    ["prettier", "--write", tmp_path],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )

                with open(tmp_path, "r") as f:
                    formatted_content = f.read()

                changes_made = formatted_content != content

                return FormatResult(
                    file_path=file_path,
                    formatter="prettier",
                    status="success" if result.returncode == 0 else "failed",
                    message=result.stderr if result.stderr else None,
                    formatted_content=formatted_content if changes_made else None,
                    changes_made=changes_made,
                )
            finally:
                os.unlink(tmp_path)

        except FileNotFoundError:
            return FormatResult(
                file_path=file_path,
                formatter="prettier",
                status="skipped",
                message="Prettier not installed",
                changes_made=False,
            )
        except Exception as e:
            return FormatResult(
                file_path=file_path,
                formatter="prettier",
                status="failed",
                message=str(e),
                changes_made=False,
            )

    def check_formatter_availability(self) -> Dict[str, bool]:
        """Check which formatters are available"""
        formatters_to_check = ["black", "ruff", "prettier"]
        availability = {}

        for formatter in formatters_to_check:
            try:
                result = subprocess.run(
                    [formatter, "--version"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                availability[formatter] = result.returncode == 0
            except (FileNotFoundError, subprocess.TimeoutExpired):
                availability[formatter] = False

        return availability
