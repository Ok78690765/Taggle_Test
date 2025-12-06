"""Code analysis service with heuristic-based analysis"""

import re
import time

from app.schemas.analysis import (
    ArchitectureInsightSchema,
    ComplexityMetricsSchema,
    DebugInsightSchema,
    FormattingRecommendationSchema,
    IssueSchema,
    QualityScoreSchema,
)
from app.utils.language_adapter import LanguageAdapterFactory


class CodeAnalyzer:
    """Service for analyzing code with various metrics and insights"""

    def __init__(self):
        self.factory = LanguageAdapterFactory()

    def analyze_quality(self, code: str, language: str) -> QualityScoreSchema:
        """Analyze code quality and return quality scores"""
        adapter = self.factory.create(language)

        lines = code.split("\n")
        total_lines = len(lines)
        blank_lines = adapter.count_blank_lines(code)
        comment_lines = len(adapter.extract_comments(code))
        code_lines = total_lines - blank_lines

        functions = adapter.extract_functions(code)
        classes = adapter.extract_classes(code)

        complexity_score = self._calculate_cyclomatic_complexity(code, language)
        duplication_score = self._calculate_duplication_score(code)
        documentation_ratio = (
            (comment_lines / code_lines * 100) if code_lines > 0 else 0
        )

        maintainability = min(
            100, 50 + documentation_ratio + (100 - complexity_score) * 0.5
        )

        code_quality = max(
            0,
            100
            - (
                (total_lines / 1000 * 5)
                + (complexity_score * 0.3)
                + (100 - duplication_score) * 0.2
            ),
        )

        overall_score = (code_quality + maintainability + duplication_score) / 3

        return QualityScoreSchema(
            overall_score=min(100, max(0, overall_score)),
            code_quality=min(100, max(0, code_quality)),
            maintainability=min(100, max(0, maintainability)),
            complexity=min(100, max(0, complexity_score)),
            duplication=duplication_score,
        )

    def analyze_issues(self, code: str, language: str) -> list[IssueSchema]:
        """Detect issues in code"""
        issues = []
        adapter = self.factory.create(language)

        issues.extend(self._detect_style_issues(code, language))
        issues.extend(self._detect_complexity_issues(code, language))
        issues.extend(self._detect_naming_issues(code, language))

        return issues

    def analyze_complexity(self, code: str, language: str) -> ComplexityMetricsSchema:
        """Analyze code complexity metrics"""
        cyclomatic_complexity = self._calculate_cyclomatic_complexity(code, language)
        cognitive_complexity = self._calculate_cognitive_complexity(code, language)
        lines_of_code = len(code.split("\n"))
        nesting_depth = self._calculate_nesting_depth(code, language)

        return ComplexityMetricsSchema(
            cyclomatic_complexity=cyclomatic_complexity,
            cognitive_complexity=cognitive_complexity,
            lines_of_code=lines_of_code,
            nesting_depth=nesting_depth,
        )

    def analyze_architecture(
        self, code: str, language: str
    ) -> list[ArchitectureInsightSchema]:
        """Analyze architectural patterns and insights"""
        insights = []

        if self._detect_singleton_pattern(code, language):
            insights.append(
                ArchitectureInsightSchema(
                    pattern_detected="Singleton Pattern",
                    confidence=0.85,
                    description="Code appears to implement the Singleton design pattern",
                    recommendations=[
                        "Ensure thread-safety is properly implemented",
                        "Consider if eager or lazy initialization is appropriate",
                    ],
                )
            )

        if self._detect_factory_pattern(code, language):
            insights.append(
                ArchitectureInsightSchema(
                    pattern_detected="Factory Pattern",
                    confidence=0.8,
                    description="Code appears to implement the Factory design pattern",
                    recommendations=[
                        "Ensure consistent creation logic",
                        "Consider abstracting further for better extensibility",
                    ],
                )
            )

        if self._detect_observer_pattern(code, language):
            insights.append(
                ArchitectureInsightSchema(
                    pattern_detected="Observer Pattern",
                    confidence=0.75,
                    description="Code appears to implement the Observer design pattern",
                    recommendations=[
                        "Ensure proper cleanup of observers",
                        "Consider weak references for listeners",
                    ],
                )
            )

        layering = self._detect_layering_issues(code)
        if layering:
            insights.extend(layering)

        return insights

    def analyze_formatting(
        self, code: str, language: str
    ) -> list[FormattingRecommendationSchema]:
        """Analyze formatting and style recommendations"""
        recommendations = []

        if language.lower() in ["python", "py"]:
            recommendations.extend(self._check_python_formatting(code))
        elif language.lower() in ["javascript", "js", "typescript", "ts"]:
            recommendations.extend(self._check_javascript_formatting(code))
        elif language.lower() == "java":
            recommendations.extend(self._check_java_formatting(code))

        return recommendations

    def analyze_for_debugging(
        self, code: str, language: str
    ) -> list[DebugInsightSchema]:
        """Analyze code for potential debugging issues"""
        insights = []

        if self._detect_uninitialized_variables(code, language):
            insights.append(
                DebugInsightSchema(
                    potential_issue="Potential uninitialized variable usage",
                    severity="warning",
                    affected_areas=["Variable assignments and usage"],
                    debug_steps=[
                        "Check variable declarations",
                        "Trace all execution paths",
                        "Add initialization checks",
                    ],
                )
            )

        if self._detect_null_pointer_risks(code, language):
            insights.append(
                DebugInsightSchema(
                    potential_issue="Potential null pointer or undefined reference",
                    severity="warning",
                    affected_areas=["Object references"],
                    debug_steps=[
                        "Add null/undefined checks",
                        "Use optional chaining where applicable",
                        "Add type guards",
                    ],
                )
            )

        if self._detect_infinite_loops(code, language):
            insights.append(
                DebugInsightSchema(
                    potential_issue="Potential infinite loop detected",
                    severity="error",
                    affected_areas=["Loop constructs"],
                    debug_steps=[
                        "Review loop conditions",
                        "Check loop increment/decrement",
                        "Add loop counters",
                    ],
                )
            )

        if self._detect_resource_leaks(code, language):
            insights.append(
                DebugInsightSchema(
                    potential_issue="Potential resource leak (file, connection, etc.)",
                    severity="warning",
                    affected_areas=["Resource management"],
                    debug_steps=[
                        "Check resource closing",
                        "Use context managers/try-finally",
                        "Add cleanup logic",
                    ],
                )
            )

        return insights

    def _calculate_cyclomatic_complexity(self, code: str, language: str) -> float:
        """Calculate cyclomatic complexity"""
        complexity = 1
        decision_patterns = [
            r"\bif\b",
            r"\belse\b",
            r"\belif\b",
            r"\bfor\b",
            r"\bwhile\b",
            r"\bcase\b",
            r"\bcatch\b",
            r"\?.*:",
        ]

        for pattern in decision_patterns:
            complexity += len(re.findall(pattern, code, re.IGNORECASE))

        return min(100, complexity / 10)

    def _calculate_cognitive_complexity(self, code: str, language: str) -> float:
        """Calculate cognitive complexity"""
        nesting = self._calculate_nesting_depth(code, language)
        conditionals = len(re.findall(r"\b(if|for|while|case)\b", code, re.IGNORECASE))
        cognitive = 1 + conditionals + nesting * 2

        return min(100, cognitive / 2)

    def _calculate_nesting_depth(self, code: str, language: str) -> int:
        """Calculate maximum nesting depth"""
        max_depth = 0
        current_depth = 0

        for char in code:
            if char in "{([":
                current_depth += 1
                max_depth = max(max_depth, current_depth)
            elif char in "}])":
                current_depth = max(0, current_depth - 1)

        return max_depth

    def _calculate_duplication_score(self, code: str) -> float:
        """Calculate code duplication score (lower duplication = higher score)"""
        lines = code.split("\n")
        unique_lines = len(set(lines))
        total_lines = len(lines)

        if total_lines == 0:
            return 100

        duplication_ratio = 1 - (unique_lines / total_lines)
        return max(0, 100 - duplication_ratio * 100)

    def _detect_style_issues(self, code: str, language: str) -> list[IssueSchema]:
        """Detect style issues"""
        issues = []

        long_lines = [
            (i + 1, len(line))
            for i, line in enumerate(code.split("\n"))
            if len(line) > 100
        ]

        for line_num, length in long_lines[:5]:
            issues.append(
                IssueSchema(
                    issue_type="style",
                    severity="info",
                    line_number=line_num,
                    message=f"Line exceeds 100 characters ({length} chars)",
                    suggestion="Consider breaking this line for better readability",
                )
            )

        return issues

    def _detect_complexity_issues(self, code: str, language: str) -> list[IssueSchema]:
        """Detect high-complexity code sections"""
        issues = []
        complexity = self._calculate_cyclomatic_complexity(code, language)

        if complexity > 50:
            issues.append(
                IssueSchema(
                    issue_type="complexity",
                    severity="warning",
                    message="High cyclomatic complexity detected",
                    suggestion="Consider refactoring into smaller functions",
                )
            )

        nesting = self._calculate_nesting_depth(code, language)
        if nesting > 5:
            issues.append(
                IssueSchema(
                    issue_type="nesting",
                    severity="warning",
                    message=f"Deep nesting detected (level {nesting})",
                    suggestion="Consider extracting nested blocks into separate functions",
                )
            )

        return issues

    def _detect_naming_issues(self, code: str, language: str) -> list[IssueSchema]:
        """Detect naming convention issues"""
        issues = []

        single_letter_vars = re.findall(r"\b[a-z]\b(?!\w)", code)
        if len(single_letter_vars) > 3:
            issues.append(
                IssueSchema(
                    issue_type="naming",
                    severity="info",
                    message=f"Multiple single-letter variable names found",
                    suggestion="Use more descriptive variable names",
                )
            )

        return issues

    def _detect_singleton_pattern(self, code: str, language: str) -> bool:
        """Detect Singleton design pattern"""
        singleton_indicators = [
            r"private\s+static\s+\w+\s+instance",
            r"getInstance\s*\(",
            r"private\s+def\s+__init__",
        ]

        for pattern in singleton_indicators:
            if re.search(pattern, code):
                return True

        return False

    def _detect_factory_pattern(self, code: str, language: str) -> bool:
        """Detect Factory design pattern"""
        factory_indicators = [
            r"create\w+\s*\(",
            r"make\w+\s*\(",
            r"build\w+\s*\(",
            r"Factory\s*class",
        ]

        for pattern in factory_indicators:
            if re.search(pattern, code):
                return True

        return False

    def _detect_observer_pattern(self, code: str, language: str) -> bool:
        """Detect Observer design pattern"""
        observer_indicators = [
            r"subscribe\s*\(",
            r"addListener\s*\(",
            r"addEventListener\s*\(",
            r"notify\s*\(",
            r"emit\s*\(",
        ]

        for pattern in observer_indicators:
            if re.search(pattern, code):
                return True

        return False

    def _detect_layering_issues(self, code: str) -> list[ArchitectureInsightSchema]:
        """Detect architectural layering issues"""
        insights = []

        if self._has_mixed_concerns(code):
            insights.append(
                ArchitectureInsightSchema(
                    pattern_detected="Mixed Concerns",
                    confidence=0.7,
                    description="Code appears to mix multiple concerns in a single module",
                    recommendations=[
                        "Consider separating presentation, business logic, and data layers",
                        "Apply Single Responsibility Principle",
                    ],
                )
            )

        return insights

    def _has_mixed_concerns(self, code: str) -> bool:
        """Check if code has mixed concerns"""
        db_patterns = [
            r"SELECT|INSERT|UPDATE|DELETE|query|execute",
            r"\.save\(|\.delete\(",
        ]
        ui_patterns = [r"render|display|button|click|onChange|setState"]
        logic_patterns = [r"calculate|process|validate|transform"]

        db_count = sum(len(re.findall(p, code)) for p in db_patterns)
        ui_count = sum(len(re.findall(p, code)) for p in ui_patterns)
        logic_count = sum(len(re.findall(p, code)) for p in logic_patterns)

        return (db_count > 0 and ui_count > 0) or (db_count > 0 and logic_count > 5)

    def _check_python_formatting(
        self, code: str
    ) -> list[FormattingRecommendationSchema]:
        """Check Python formatting recommendations"""
        recommendations = []

        spaces = len(re.findall(r"^\t", code, re.MULTILINE))
        if spaces > 0:
            recommendations.append(
                FormattingRecommendationSchema(
                    category="indentation",
                    current_style="tabs",
                    recommended_style="spaces (4 spaces per level)",
                    reason="PEP 8 recommends using spaces for indentation",
                )
            )

        return recommendations

    def _check_javascript_formatting(
        self, code: str
    ) -> list[FormattingRecommendationSchema]:
        """Check JavaScript/TypeScript formatting recommendations"""
        recommendations = []

        no_semicolon = len(re.findall(r"[^;{\s]\n", code))
        semicolon = len(re.findall(r";", code))

        if semicolon == 0 and no_semicolon > 3:
            recommendations.append(
                FormattingRecommendationSchema(
                    category="semicolons",
                    current_style="no semicolons",
                    recommended_style="semicolons at line endings",
                    reason="Consistent semicolon usage prevents potential ASI issues",
                )
            )

        return recommendations

    def _check_java_formatting(self, code: str) -> list[FormattingRecommendationSchema]:
        """Check Java formatting recommendations"""
        recommendations = []

        if not re.search(r"{\s*$", code, re.MULTILINE):
            recommendations.append(
                FormattingRecommendationSchema(
                    category="brace_style",
                    current_style="braces on new line",
                    recommended_style="braces at end of line",
                    reason="Java convention places opening braces at line end",
                )
            )

        return recommendations

    def _detect_uninitialized_variables(self, code: str, language: str) -> bool:
        """Detect potential uninitialized variable usage"""
        patterns = [r"if\s+\w+\s*[=!]", r"return\s+\w+", r"\w+\s*\+="]
        return any(re.search(p, code) for p in patterns)

    def _detect_null_pointer_risks(self, code: str, language: str) -> bool:
        """Detect null pointer or undefined reference risks"""
        patterns = [
            r"\.\w+\s*\(",
            r"\[\d+\]",
            r"\.split\(|\.join\(|\.map\(",
        ]
        total_matches = sum(len(re.findall(pattern, code)) for pattern in patterns)
        return total_matches > 5

    def _detect_infinite_loops(self, code: str, language: str) -> bool:
        """Detect potential infinite loops"""
        while_true_py = bool(re.search(r"while\s+[Tt]rue\s*:", code))
        while_true_js = bool(re.search(r"while\s*\(\s*[Tt]rue\s*\)", code))
        for_without_change = bool(re.search(r"for\s*\([^;]*;[^;]*;\s*\)", code))

        return while_true_py or while_true_js or for_without_change

    def _detect_resource_leaks(self, code: str, language: str) -> bool:
        """Detect potential resource leaks"""
        patterns = [r"open\s*\(", r"\.connect\s*\(", r"new\s+FileStream"]
        no_context = not bool(re.search(r"with\s+|try\s*\{|finally\s*\{", code))

        return any(re.search(p, code) for p in patterns) and no_context


class AnalysisService:
    """Service orchestrating code analysis"""

    def __init__(self):
        self.analyzer = CodeAnalyzer()

    def analyze_full(self, code: str, language: str, file_name: str | None = None):
        """Perform full code analysis"""
        start_time = time.time()

        quality_score = self.analyzer.analyze_quality(code, language)
        issues = self.analyzer.analyze_issues(code, language)
        complexity = self.analyzer.analyze_complexity(code, language)
        architecture = self.analyzer.analyze_architecture(code, language)
        formatting = self.analyzer.analyze_formatting(code, language)

        duration = (time.time() - start_time) * 1000

        return {
            "file_name": file_name,
            "language": language,
            "code_length": len(code.split("\n")),
            "quality_score": quality_score,
            "issues": issues,
            "complexity_metrics": complexity,
            "architecture_insights": architecture,
            "formatting_recommendations": formatting,
            "analysis_duration_ms": duration,
        }

    def analyze_for_debugging(
        self, code: str, language: str, file_name: str | None = None
    ):
        """Perform debugging-focused analysis"""
        start_time = time.time()

        debug_insights = self.analyzer.analyze_for_debugging(code, language)

        issues = self.analyzer.analyze_issues(code, language)
        common_issues = list(set(issue.message for issue in issues))

        duration = (time.time() - start_time) * 1000

        return {
            "file_name": file_name,
            "language": language,
            "debug_insights": debug_insights,
            "common_issues": common_issues,
            "analysis_duration_ms": duration,
        }
