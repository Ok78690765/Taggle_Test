"""Service for running tests as part of the prompt edit workflow"""

import os
import shlex
import subprocess
import time
from typing import List, Optional, Tuple

from app.schemas.prompt_edit import TestRunResponse


class TestRunnerService:
    """Service for executing tests and capturing results"""

    def __init__(self, repo_root: Optional[str] = None):
        self.repo_root = repo_root or os.getenv("REPO_ROOT", "/home/engine/project")

    def run_tests(
        self,
        session_id: str,
        test_command: Optional[str] = None,
        test_paths: Optional[List[str]] = None,
        coverage: bool = False,
    ) -> TestRunResponse:
        """
        Run tests and return results

        Args:
            session_id: Session identifier
            test_command: Optional custom test command
            test_paths: Specific test paths to run
            coverage: Whether to collect coverage

        Returns:
            TestRunResponse with test results
        """
        command = self._build_command(test_command, test_paths, coverage)
        start_time = time.time()

        try:
            process = subprocess.run(
                command,
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                timeout=1800,
            )
            duration = time.time() - start_time

            status = "passed" if process.returncode == 0 else "failed"

            passed, failed, skipped = self._parse_test_output(process.stdout)

            return TestRunResponse(
                session_id=session_id,
                status=status,
                passed=passed,
                failed=failed,
                skipped=skipped,
                duration=duration,
                output=process.stdout + "\n" + process.stderr,
                coverage_percent=self._extract_coverage_percent(process.stdout)
                if coverage
                else None,
            )
        except subprocess.TimeoutExpired as e:
            duration = time.time() - start_time
            return TestRunResponse(
                session_id=session_id,
                status="failed",
                passed=0,
                failed=0,
                skipped=0,
                duration=duration,
                output=f"Test command timed out: {str(e)}",
            )
        except Exception as e:
            duration = time.time() - start_time
            return TestRunResponse(
                session_id=session_id,
                status="failed",
                passed=0,
                failed=0,
                skipped=0,
                duration=duration,
                output=str(e),
            )

    def _build_command(
        self,
        test_command: Optional[str],
        test_paths: Optional[List[str]],
        coverage: bool,
    ) -> List[str]:
        """Build the test command to run"""
        if test_command:
            if isinstance(test_command, str):
                return shlex.split(test_command)
            return test_command

        base_command = ["python", "-m", "pytest"]

        if coverage:
            base_command = [
                "coverage",
                "run",
                "-m",
                "pytest",
            ]

        if test_paths:
            base_command.extend(test_paths)

        return base_command

    def _parse_test_output(self, output: str) -> Tuple[int, int, int]:
        """Parse pytest output to extract pass/fail counts"""
        passed = failed = skipped = 0

        for line in output.splitlines():
            line = line.strip().lower()
            if line.startswith("===") and "in" in line and "collected" in line:
                # Example: "=== 5 passed, 2 warnings in 0.50s ==="
                parts = line.replace("===", "").split(",")
                for part in parts:
                    part = part.strip()
                    if "passed" in part:
                        passed += int(part.split()[0])
                    elif "failed" in part:
                        failed += int(part.split()[0])
                    elif "skipped" in part:
                        skipped += int(part.split()[0])

        return passed, failed, skipped

    def _extract_coverage_percent(self, output: str) -> Optional[float]:
        """Extract coverage percentage from output"""
        match = None
        for line in output.splitlines():
            line = line.strip().lower()
            if "coverage" in line and "%" in line:
                # Recognize patterns like "TOTAL 100 90 90%"
                tokens = line.split()
                for token in tokens:
                    if token.endswith("%"):
                        try:
                            return float(token.strip("%"))
                        except ValueError:
                            continue
        return None
