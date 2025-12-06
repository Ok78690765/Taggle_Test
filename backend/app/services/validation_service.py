"""Service for validating code edits"""

import ast
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List

from app.schemas.prompt_edit import ValidationResult


class ValidationService:
    """Service for validating code changes"""

    def validate_syntax(self, file_path: str, content: str) -> ValidationResult:
        """
        Validate code syntax

        Args:
            file_path: Path to the file
            content: File content to validate

        Returns:
            ValidationResult with syntax validation status
        """
        language = self._detect_language(file_path)

        if language == "python":
            return self._validate_python_syntax(file_path, content)
        elif language in ["javascript", "typescript"]:
            return self._validate_javascript_syntax(file_path, content)
        else:
            return ValidationResult(
                validation_type="syntax",
                status="pass",
                file_path=file_path,
                message=f"Syntax validation not available for {language}",
            )

    def validate_lint(self, file_path: str, content: str) -> ValidationResult:
        """
        Validate code with linters

        Args:
            file_path: Path to the file
            content: File content to validate

        Returns:
            ValidationResult with lint validation status
        """
        language = self._detect_language(file_path)

        if language == "python":
            return self._lint_python(file_path, content)
        elif language in ["javascript", "typescript"]:
            return self._lint_javascript(file_path, content)
        else:
            return ValidationResult(
                validation_type="lint",
                status="pass",
                file_path=file_path,
                message=f"Linting not available for {language}",
            )

    def validate_type_check(self, file_path: str, content: str) -> ValidationResult:
        """
        Validate type checking

        Args:
            file_path: Path to the file
            content: File content to validate

        Returns:
            ValidationResult with type check status
        """
        language = self._detect_language(file_path)

        if language == "python":
            return self._typecheck_python(file_path, content)
        elif language == "typescript":
            return self._typecheck_typescript(file_path, content)
        else:
            return ValidationResult(
                validation_type="type",
                status="pass",
                file_path=file_path,
                message=f"Type checking not available for {language}",
            )

    def validate_all(self, file_path: str, content: str) -> List[ValidationResult]:
        """
        Run all validations on a file

        Args:
            file_path: Path to the file
            content: File content to validate

        Returns:
            List of ValidationResults
        """
        return [
            self.validate_syntax(file_path, content),
            self.validate_lint(file_path, content),
            self.validate_type_check(file_path, content),
        ]

    def _detect_language(self, file_path: str) -> str:
        """Detect language from file extension"""
        ext = Path(file_path).suffix.lstrip(".")
        language_map = {
            "py": "python",
            "js": "javascript",
            "jsx": "javascript",
            "ts": "typescript",
            "tsx": "typescript",
        }
        return language_map.get(ext, "unknown")

    def _validate_python_syntax(
        self, file_path: str, content: str
    ) -> ValidationResult:
        """Validate Python syntax using AST"""
        try:
            ast.parse(content)
            return ValidationResult(
                validation_type="syntax",
                status="pass",
                file_path=file_path,
                message="Python syntax is valid",
            )
        except SyntaxError as e:
            return ValidationResult(
                validation_type="syntax",
                status="fail",
                file_path=file_path,
                message=f"Syntax error at line {e.lineno}: {e.msg}",
                details={"line": e.lineno, "offset": e.offset, "text": e.text},
            )

    def _validate_javascript_syntax(
        self, file_path: str, content: str
    ) -> ValidationResult:
        """Validate JavaScript/TypeScript syntax"""
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=Path(file_path).suffix, delete=False
            ) as tmp:
                tmp.write(content)
                tmp_path = tmp.name

            try:
                result = subprocess.run(
                    ["node", "--check", tmp_path],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )

                if result.returncode == 0:
                    return ValidationResult(
                        validation_type="syntax",
                        status="pass",
                        file_path=file_path,
                        message="JavaScript syntax is valid",
                    )
                else:
                    return ValidationResult(
                        validation_type="syntax",
                        status="fail",
                        file_path=file_path,
                        message=result.stderr,
                    )
            finally:
                import os

                os.unlink(tmp_path)

        except FileNotFoundError:
            return ValidationResult(
                validation_type="syntax",
                status="pass",
                file_path=file_path,
                message="Node.js not available for syntax checking",
            )
        except Exception as e:
            return ValidationResult(
                validation_type="syntax",
                status="fail",
                file_path=file_path,
                message=str(e),
            )

    def _lint_python(self, file_path: str, content: str) -> ValidationResult:
        """Lint Python code with pylint"""
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".py", delete=False
            ) as tmp:
                tmp.write(content)
                tmp_path = tmp.name

            try:
                result = subprocess.run(
                    ["pylint", "--output-format=text", tmp_path],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )

                if result.returncode == 0:
                    status = "pass"
                    message = "No linting issues found"
                elif result.returncode < 16:
                    status = "warning"
                    message = result.stdout[:500]
                else:
                    status = "fail"
                    message = result.stdout[:500]

                return ValidationResult(
                    validation_type="lint",
                    status=status,
                    file_path=file_path,
                    message=message,
                )
            finally:
                import os

                os.unlink(tmp_path)

        except FileNotFoundError:
            return ValidationResult(
                validation_type="lint",
                status="pass",
                file_path=file_path,
                message="Pylint not installed",
            )
        except Exception as e:
            return ValidationResult(
                validation_type="lint",
                status="fail",
                file_path=file_path,
                message=str(e),
            )

    def _lint_javascript(self, file_path: str, content: str) -> ValidationResult:
        """Lint JavaScript/TypeScript code"""
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=Path(file_path).suffix, delete=False
            ) as tmp:
                tmp.write(content)
                tmp_path = tmp.name

            try:
                result = subprocess.run(
                    ["eslint", tmp_path],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )

                if result.returncode == 0:
                    return ValidationResult(
                        validation_type="lint",
                        status="pass",
                        file_path=file_path,
                        message="No linting issues found",
                    )
                else:
                    return ValidationResult(
                        validation_type="lint",
                        status="warning",
                        file_path=file_path,
                        message=result.stdout[:500],
                    )
            finally:
                import os

                os.unlink(tmp_path)

        except FileNotFoundError:
            return ValidationResult(
                validation_type="lint",
                status="pass",
                file_path=file_path,
                message="ESLint not installed",
            )
        except Exception as e:
            return ValidationResult(
                validation_type="lint",
                status="fail",
                file_path=file_path,
                message=str(e),
            )

    def _typecheck_python(self, file_path: str, content: str) -> ValidationResult:
        """Type check Python code with mypy"""
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".py", delete=False
            ) as tmp:
                tmp.write(content)
                tmp_path = tmp.name

            try:
                result = subprocess.run(
                    ["mypy", "--ignore-missing-imports", tmp_path],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )

                if result.returncode == 0:
                    return ValidationResult(
                        validation_type="type",
                        status="pass",
                        file_path=file_path,
                        message="No type errors found",
                    )
                else:
                    return ValidationResult(
                        validation_type="type",
                        status="warning",
                        file_path=file_path,
                        message=result.stdout[:500],
                    )
            finally:
                import os

                os.unlink(tmp_path)

        except FileNotFoundError:
            return ValidationResult(
                validation_type="type",
                status="pass",
                file_path=file_path,
                message="Mypy not installed",
            )
        except Exception as e:
            return ValidationResult(
                validation_type="type",
                status="fail",
                file_path=file_path,
                message=str(e),
            )

    def _typecheck_typescript(self, file_path: str, content: str) -> ValidationResult:
        """Type check TypeScript code"""
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".ts", delete=False
            ) as tmp:
                tmp.write(content)
                tmp_path = tmp.name

            try:
                result = subprocess.run(
                    ["tsc", "--noEmit", tmp_path],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )

                if result.returncode == 0:
                    return ValidationResult(
                        validation_type="type",
                        status="pass",
                        file_path=file_path,
                        message="No type errors found",
                    )
                else:
                    return ValidationResult(
                        validation_type="type",
                        status="warning",
                        file_path=file_path,
                        message=result.stdout[:500],
                    )
            finally:
                import os

                os.unlink(tmp_path)

        except FileNotFoundError:
            return ValidationResult(
                validation_type="type",
                status="pass",
                file_path=file_path,
                message="TypeScript compiler not installed",
            )
        except Exception as e:
            return ValidationResult(
                validation_type="type",
                status="fail",
                file_path=file_path,
                message=str(e),
            )
