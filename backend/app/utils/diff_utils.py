"""Utilities for generating and working with diffs"""

import difflib
from typing import List, Tuple


def generate_unified_diff(
    original: str,
    modified: str,
    file_path: str = "file",
    fromfile: str = "original",
    tofile: str = "modified",
    lineterm: str = "",
) -> str:
    """
    Generate unified diff between two strings

    Args:
        original: Original content
        modified: Modified content
        file_path: File path for context
        fromfile: Label for original file
        tofile: Label for modified file
        lineterm: Line terminator

    Returns:
        Unified diff string
    """
    original_lines = original.splitlines(keepends=True)
    modified_lines = modified.splitlines(keepends=True)

    diff = difflib.unified_diff(
        original_lines,
        modified_lines,
        fromfile=f"{fromfile}/{file_path}",
        tofile=f"{tofile}/{file_path}",
        lineterm=lineterm,
    )

    return "".join(diff)


def count_diff_changes(diff: str) -> Tuple[int, int]:
    """
    Count additions and deletions in a unified diff

    Args:
        diff: Unified diff string

    Returns:
        Tuple of (additions, deletions)
    """
    additions = 0
    deletions = 0

    for line in diff.split("\n"):
        if line.startswith("+") and not line.startswith("+++"):
            additions += 1
        elif line.startswith("-") and not line.startswith("---"):
            deletions += 1

    return additions, deletions


def apply_patch(original: str, diff: str) -> str:
    """
    Apply a unified diff patch to original content

    Args:
        original: Original content
        diff: Unified diff to apply

    Returns:
        Patched content

    Raises:
        ValueError: If patch cannot be applied
    """
    original_lines = original.splitlines(keepends=True)
    diff_lines = diff.splitlines(keepends=True)

    try:
        patches = difflib.unified_diff_to_delta(diff_lines)
        result = difflib.restore(patches, 2)
        return "".join(result)
    except Exception as e:
        raise ValueError(f"Failed to apply patch: {str(e)}")


def format_diff_for_display(diff: str, context_lines: int = 3) -> List[str]:
    """
    Format diff for better display with syntax highlighting markers

    Args:
        diff: Unified diff string
        context_lines: Number of context lines to show

    Returns:
        List of formatted diff lines with markers
    """
    formatted = []
    for line in diff.split("\n"):
        if line.startswith("+++") or line.startswith("---"):
            formatted.append(("header", line))
        elif line.startswith("@@"):
            formatted.append(("hunk", line))
        elif line.startswith("+"):
            formatted.append(("addition", line))
        elif line.startswith("-"):
            formatted.append(("deletion", line))
        else:
            formatted.append(("context", line))

    return formatted


def get_changed_line_numbers(diff: str) -> Tuple[List[int], List[int]]:
    """
    Extract line numbers that were changed in the diff

    Args:
        diff: Unified diff string

    Returns:
        Tuple of (original_lines, modified_lines)
    """
    original_lines = []
    modified_lines = []
    current_original = 0
    current_modified = 0

    for line in diff.split("\n"):
        if line.startswith("@@"):
            # Parse hunk header: @@ -start,count +start,count @@
            parts = line.split()
            if len(parts) >= 3:
                original_part = parts[1].lstrip("-").split(",")
                modified_part = parts[2].lstrip("+").split(",")
                current_original = int(original_part[0])
                current_modified = int(modified_part[0])
        elif line.startswith("-") and not line.startswith("---"):
            original_lines.append(current_original)
            current_original += 1
        elif line.startswith("+") and not line.startswith("+++"):
            modified_lines.append(current_modified)
            current_modified += 1
        elif line and not line.startswith("\\"):
            current_original += 1
            current_modified += 1

    return original_lines, modified_lines
