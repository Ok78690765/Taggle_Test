"""Language adapters for parsing different programming languages"""

import re
from abc import ABC, abstractmethod
from typing import Any


class LanguageAdapter(ABC):
    """Abstract base class for language adapters"""

    language: str

    @abstractmethod
    def extract_functions(self, code: str) -> list[dict[str, Any]]:
        """Extract function definitions from code"""
        pass

    @abstractmethod
    def extract_classes(self, code: str) -> list[dict[str, Any]]:
        """Extract class definitions from code"""
        pass

    @abstractmethod
    def extract_imports(self, code: str) -> list[str]:
        """Extract import statements from code"""
        pass

    @abstractmethod
    def extract_comments(self, code: str) -> list[dict[str, Any]]:
        """Extract comments from code"""
        pass

    def count_lines(self, code: str) -> int:
        """Count total lines of code"""
        return len(code.split("\n"))

    def count_blank_lines(self, code: str) -> int:
        """Count blank lines"""
        return len([line for line in code.split("\n") if not line.strip()])

    def count_comment_lines(self, code: str) -> list[dict[str, Any]]:
        """Count comment lines"""
        return self.extract_comments(code)


class PythonAdapter(LanguageAdapter):
    """Adapter for Python language"""

    language = "python"

    def extract_functions(self, code: str) -> list[dict[str, Any]]:
        """Extract function definitions"""
        pattern = r"^\s*def\s+(\w+)\s*\((.*?)\)"
        matches = []
        for i, line in enumerate(code.split("\n"), 1):
            match = re.match(pattern, line)
            if match:
                matches.append(
                    {
                        "name": match.group(1),
                        "line": i,
                        "parameters": [
                            p.strip() for p in match.group(2).split(",") if p.strip()
                        ],
                    }
                )
        return matches

    def extract_classes(self, code: str) -> list[dict[str, Any]]:
        """Extract class definitions"""
        pattern = r"^\s*class\s+(\w+)\s*(\(.*?\))?"
        matches = []
        for i, line in enumerate(code.split("\n"), 1):
            match = re.match(pattern, line)
            if match:
                matches.append(
                    {
                        "name": match.group(1),
                        "line": i,
                        "bases": match.group(2) if match.group(2) else "",
                    }
                )
        return matches

    def extract_imports(self, code: str) -> list[str]:
        """Extract import statements"""
        pattern = r"^\s*(from|import)\s+(.+)$"
        imports = []
        for line in code.split("\n"):
            match = re.match(pattern, line)
            if match:
                imports.append(line.strip())
        return imports

    def extract_comments(self, code: str) -> list[dict[str, Any]]:
        """Extract comments"""
        comments = []
        for i, line in enumerate(code.split("\n"), 1):
            stripped = line.strip()
            if stripped.startswith("#"):
                comments.append({"line": i, "text": stripped})
        return comments


class JavaScriptAdapter(LanguageAdapter):
    """Adapter for JavaScript/TypeScript language"""

    language = "javascript"

    def extract_functions(self, code: str) -> list[dict[str, Any]]:
        """Extract function definitions"""
        patterns = [
            r"function\s+(\w+)\s*\((.*?)\)",
            r"const\s+(\w+)\s*=\s*(?:async\s*)?\((.*?)\)",
            r"(\w+)\s*\((.*?)\)\s*\{",
        ]
        matches = []
        for i, line in enumerate(code.split("\n"), 1):
            for pattern in patterns:
                match = re.search(pattern, line)
                if match:
                    matches.append(
                        {
                            "name": match.group(1),
                            "line": i,
                            "parameters": [
                                p.strip()
                                for p in match.group(2).split(",")
                                if p.strip()
                            ],
                        }
                    )
                    break
        return list({m["name"]: m for m in matches}.values())

    def extract_classes(self, code: str) -> list[dict[str, Any]]:
        """Extract class definitions"""
        pattern = r"class\s+(\w+)\s*(?:extends\s+(\w+))?"
        matches = []
        for i, line in enumerate(code.split("\n"), 1):
            match = re.search(pattern, line)
            if match:
                matches.append(
                    {
                        "name": match.group(1),
                        "line": i,
                        "extends": match.group(2) if match.group(2) else None,
                    }
                )
        return matches

    def extract_imports(self, code: str) -> list[str]:
        """Extract import/require statements"""
        patterns = [
            r"^\s*import\s+.+from\s+",
            r"^\s*require\s*\(",
        ]
        imports = []
        for line in code.split("\n"):
            for pattern in patterns:
                if re.match(pattern, line):
                    imports.append(line.strip())
                    break
        return imports

    def extract_comments(self, code: str) -> list[dict[str, Any]]:
        """Extract comments"""
        comments = []
        in_block_comment = False
        for i, line in enumerate(code.split("\n"), 1):
            stripped = line.strip()

            if "/*" in stripped:
                in_block_comment = True
            if "*/" in stripped:
                in_block_comment = False
                comments.append({"line": i, "text": stripped, "type": "block"})
                continue

            if in_block_comment:
                comments.append({"line": i, "text": stripped, "type": "block"})
            elif stripped.startswith("//"):
                comments.append({"line": i, "text": stripped, "type": "line"})

        return comments


class JavaAdapter(LanguageAdapter):
    """Adapter for Java language"""

    language = "java"

    def extract_functions(self, code: str) -> list[dict[str, Any]]:
        """Extract method definitions"""
        pattern = r"(public|private|protected|static)?\s*\w+\s+(\w+)\s*\((.*?)\)\s*\{"
        matches = []
        for i, line in enumerate(code.split("\n"), 1):
            match = re.search(pattern, line)
            if match and match.group(2) != "class":
                matches.append(
                    {
                        "name": match.group(2),
                        "line": i,
                        "parameters": [
                            p.strip() for p in match.group(3).split(",") if p.strip()
                        ],
                    }
                )
        return matches

    def extract_classes(self, code: str) -> list[dict[str, Any]]:
        """Extract class definitions"""
        pattern = r"(?:public|private)?\s*class\s+(\w+)\s*(?:extends\s+(\w+))?"
        matches = []
        for i, line in enumerate(code.split("\n"), 1):
            match = re.search(pattern, line)
            if match:
                matches.append(
                    {
                        "name": match.group(1),
                        "line": i,
                        "extends": match.group(2) if match.group(2) else None,
                    }
                )
        return matches

    def extract_imports(self, code: str) -> list[str]:
        """Extract import statements"""
        pattern = r"^\s*import\s+.+;"
        imports = []
        for line in code.split("\n"):
            if re.match(pattern, line):
                imports.append(line.strip())
        return imports

    def extract_comments(self, code: str) -> list[dict[str, Any]]:
        """Extract comments"""
        comments = []
        in_block_comment = False
        for i, line in enumerate(code.split("\n"), 1):
            stripped = line.strip()

            if "/*" in stripped:
                in_block_comment = True
            if "*/" in stripped:
                in_block_comment = False
                comments.append({"line": i, "text": stripped, "type": "block"})
                continue

            if in_block_comment:
                comments.append({"line": i, "text": stripped, "type": "block"})
            elif stripped.startswith("//"):
                comments.append({"line": i, "text": stripped, "type": "line"})

        return comments


class LanguageAdapterFactory:
    """Factory for creating language adapters"""

    _adapters: dict[str, type[LanguageAdapter]] = {
        "python": PythonAdapter,
        "py": PythonAdapter,
        "javascript": JavaScriptAdapter,
        "js": JavaScriptAdapter,
        "typescript": JavaScriptAdapter,
        "ts": JavaScriptAdapter,
        "java": JavaAdapter,
        "cpp": JavaAdapter,
        "c++": JavaAdapter,
    }

    @classmethod
    def create(cls, language: str) -> LanguageAdapter:
        """Create adapter for given language"""
        adapter_class = cls._adapters.get(language.lower())
        if not adapter_class:
            raise ValueError(
                f"Unsupported language: {language}. Supported: {', '.join(cls._adapters.keys())}"
            )
        return adapter_class()

    @classmethod
    def supported_languages(cls) -> list[str]:
        """Get list of supported languages"""
        return list(cls._adapters.keys())
