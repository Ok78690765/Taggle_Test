# Code Analysis API Documentation

## Overview

The Code Analysis API provides comprehensive analysis of source code across multiple programming languages. It offers features for code quality scoring, issue detection, complexity metrics, architectural insights, and formatting recommendations.

## Features

### 1. Code Quality Scoring
- **Overall Quality Score** (0-100): Composite score reflecting general code quality
- **Code Quality Rating**: Assessment of code structure and best practices
- **Maintainability Index**: How easy the code is to understand and modify
- **Complexity Assessment**: Cyclomatic and cognitive complexity metrics
- **Duplication Score**: Measure of code repetition

### 2. Issue Detection
- **Style Issues**: Line length, formatting inconsistencies
- **Complexity Issues**: High cyclomatic complexity, deep nesting
- **Naming Issues**: Non-descriptive variable names, convention violations
- Each issue includes:
  - Severity level (error, warning, info)
  - Line and column numbers
  - Human-readable message
  - Suggested fix

### 3. Complexity Metrics
- **Cyclomatic Complexity**: Number of independent execution paths
- **Cognitive Complexity**: Mental effort required to understand code
- **Lines of Code**: Total lines including comments and blank lines
- **Nesting Depth**: Maximum nesting level of control structures

### 4. Architecture Insights
- **Design Pattern Detection**:
  - Singleton Pattern
  - Factory Pattern
  - Observer Pattern
  - Custom pattern detection
- **Layering Analysis**: Detection of mixed concerns and separation issues
- **Architectural Recommendations**: Suggestions for improvement

### 5. Formatting Recommendations
- **Indentation Style**: Spaces vs tabs
- **Semicolon Usage**: For/without semicolons
- **Brace Placement**: Opening brace placement conventions
- **Line Length**: Long line detection
- Language-specific conventions

### 6. Debugging Insights
- **Uninitialized Variables**: Potential usage of uninitialized variables
- **Null Pointer Risks**: Potential null/undefined reference issues
- **Infinite Loop Detection**: Detection of potential infinite loops
- **Resource Leak Detection**: Unclosed resources
- **Common Issues**: Aggregated issues found in code

## Supported Languages

Currently supported programming languages:
- **Python** (aliases: `python`, `py`)
- **JavaScript** (aliases: `javascript`, `js`)
- **TypeScript** (aliases: `typescript`, `ts`)
- **Java** (aliases: `java`)
- **C/C++** (aliases: `cpp`, `c++`)

## API Endpoints

### 1. Get Supported Languages
```http
GET /api/analysis/supported-languages
```

**Response:**
```json
{
  "supported_languages": ["python", "py", "javascript", "js", "typescript", "ts", "java"],
  "count": 7
}
```

### 2. Comprehensive Code Analysis
```http
POST /api/analysis/analyze
```

**Request:**
```json
{
  "code": "def hello(name):\n    return f'Hello, {name}!'",
  "language": "python",
  "file_name": "test.py",
  "analyze_quality": true,
  "analyze_issues": true,
  "analyze_architecture": true,
  "analyze_formatting": true
}
```

**Response:**
```json
{
  "file_name": "test.py",
  "language": "python",
  "code_length": 3,
  "quality_score": {
    "overall_score": 85.5,
    "code_quality": 90.0,
    "maintainability": 88.0,
    "complexity": 15.0,
    "duplication": 75.0
  },
  "issues": [
    {
      "issue_type": "style",
      "severity": "info",
      "line_number": 1,
      "message": "Line exceeds 100 characters (115 chars)",
      "suggestion": "Consider breaking this line for better readability"
    }
  ],
  "complexity_metrics": {
    "cyclomatic_complexity": 1.5,
    "cognitive_complexity": 2.0,
    "lines_of_code": 3,
    "nesting_depth": 0
  },
  "architecture_insights": [],
  "formatting_recommendations": [],
  "analysis_duration_ms": 25.3
}
```

### 3. Quality Analysis Only
```http
POST /api/analysis/analyze/quality
```

**Request:**
```json
{
  "code": "def add(a, b):\n    return a + b",
  "language": "python"
}
```

**Response:**
```json
{
  "file_name": null,
  "language": "python",
  "quality_score": {
    "overall_score": 92.0,
    "code_quality": 95.0,
    "maintainability": 92.0,
    "complexity": 10.0,
    "duplication": 85.0
  }
}
```

### 4. Issue Detection
```http
POST /api/analysis/analyze/issues
```

**Request:**
```json
{
  "code": "def complex_func(a,b,c,d):\n    if a: ...",
  "language": "python"
}
```

**Response:**
```json
{
  "file_name": null,
  "language": "python",
  "issues": [
    {
      "issue_type": "complexity",
      "severity": "warning",
      "line_number": null,
      "message": "High cyclomatic complexity detected",
      "suggestion": "Consider refactoring into smaller functions"
    }
  ],
  "total_issues": 1
}
```

### 5. Complexity Metrics
```http
POST /api/analysis/analyze/complexity
```

**Request:**
```json
{
  "code": "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)",
  "language": "python"
}
```

**Response:**
```json
{
  "file_name": null,
  "language": "python",
  "complexity_metrics": {
    "cyclomatic_complexity": 2.0,
    "cognitive_complexity": 4.0,
    "lines_of_code": 4,
    "nesting_depth": 1
  }
}
```

### 6. Architecture Analysis
```http
POST /api/analysis/analyze/architecture
```

**Request:**
```json
{
  "code": "class Singleton:\n    _instance = None\n    def __new__(cls):\n        if cls._instance is None:\n            cls._instance = super().__new__(cls)\n        return cls._instance",
  "language": "python"
}
```

**Response:**
```json
{
  "file_name": null,
  "language": "python",
  "architecture_insights": [
    {
      "pattern_detected": "Singleton Pattern",
      "confidence": 0.85,
      "description": "Code appears to implement the Singleton design pattern",
      "recommendations": [
        "Ensure thread-safety is properly implemented",
        "Consider if eager or lazy initialization is appropriate"
      ]
    }
  ]
}
```

### 7. Formatting Recommendations
```http
POST /api/analysis/analyze/formatting
```

**Request:**
```json
{
  "code": "def test():\n\tx = 1",
  "language": "python"
}
```

**Response:**
```json
{
  "file_name": null,
  "language": "python",
  "formatting_recommendations": [
    {
      "category": "indentation",
      "current_style": "tabs",
      "recommended_style": "spaces (4 spaces per level)",
      "reason": "PEP 8 recommends using spaces for indentation"
    }
  ]
}
```

### 8. Debugging Analysis
```http
POST /api/analysis/analyze/debug
```

**Request:**
```json
{
  "code": "def risky():\n    while True:\n        f = open('file.txt')\n        print(f.read())",
  "language": "python"
}
```

**Response:**
```json
{
  "file_name": null,
  "language": "python",
  "debug_insights": [
    {
      "potential_issue": "Potential infinite loop detected",
      "severity": "error",
      "affected_areas": ["Loop constructs"],
      "debug_steps": [
        "Review loop conditions",
        "Check loop increment/decrement",
        "Add loop counters"
      ],
      "related_line_numbers": []
    },
    {
      "potential_issue": "Potential resource leak (file, connection, etc.)",
      "severity": "warning",
      "affected_areas": ["Resource management"],
      "debug_steps": [
        "Check resource closing",
        "Use context managers/try-finally",
        "Add cleanup logic"
      ],
      "related_line_numbers": []
    }
  ],
  "common_issues": [
    "Potential infinite loop detected",
    "Potential resource leak (file, connection, etc.)"
  ],
  "analysis_duration_ms": 15.2
}
```

## Request Schema

### CodeAnalysisRequestSchema

```json
{
  "code": "string (required, min_length=1)",
  "language": "string (required)",
  "file_name": "string (optional)",
  "analyze_quality": "boolean (default: true)",
  "analyze_issues": "boolean (default: true)",
  "analyze_architecture": "boolean (default: true)",
  "analyze_formatting": "boolean (default: true)"
}
```

### Parameters

- **code**: Source code to analyze. Must be non-empty.
- **language**: Programming language. Use `/api/analysis/supported-languages` to get list.
- **file_name**: Optional file name for context and response identification.
- **analyze_quality**: Include quality scoring in analysis.
- **analyze_issues**: Include issue detection in analysis.
- **analyze_architecture**: Include architecture insights in analysis.
- **analyze_formatting**: Include formatting recommendations in analysis.

## Response Schema

### CodeAnalysisResponseSchema

```json
{
  "file_name": "string or null",
  "language": "string",
  "code_length": "integer",
  "quality_score": "QualityScoreSchema",
  "issues": "array of IssueSchema",
  "complexity_metrics": "ComplexityMetricsSchema or null",
  "architecture_insights": "array of ArchitectureInsightSchema",
  "formatting_recommendations": "array of FormattingRecommendationSchema",
  "analysis_duration_ms": "number"
}
```

### QualityScoreSchema

```json
{
  "overall_score": "number (0-100)",
  "code_quality": "number (0-100)",
  "maintainability": "number (0-100)",
  "complexity": "number (0-100)",
  "duplication": "number (0-100)"
}
```

### IssueSchema

```json
{
  "issue_type": "string (complexity, lint, style, naming)",
  "severity": "string (error, warning, info)",
  "line_number": "integer or null",
  "column_number": "integer or null",
  "message": "string",
  "suggestion": "string or null"
}
```

### ComplexityMetricsSchema

```json
{
  "cyclomatic_complexity": "number",
  "cognitive_complexity": "number",
  "lines_of_code": "integer",
  "nesting_depth": "integer"
}
```

### ArchitectureInsightSchema

```json
{
  "pattern_detected": "string",
  "confidence": "number (0-1)",
  "description": "string",
  "recommendations": "array of strings"
}
```

### FormattingRecommendationSchema

```json
{
  "category": "string",
  "current_style": "string",
  "recommended_style": "string",
  "reason": "string",
  "line_number": "integer or null"
}
```

### DebugInsightSchema

```json
{
  "potential_issue": "string",
  "severity": "string (error, warning, info)",
  "affected_areas": "array of strings",
  "debug_steps": "array of strings",
  "related_line_numbers": "array of integers"
}
```

### DebugAnalysisResponseSchema

```json
{
  "file_name": "string or null",
  "language": "string",
  "debug_insights": "array of DebugInsightSchema",
  "common_issues": "array of strings",
  "analysis_duration_ms": "number"
}
```

## Error Handling

The API returns standard HTTP status codes:

- **200 OK**: Successful analysis
- **400 Bad Request**: Invalid language or malformed request
- **422 Unprocessable Entity**: Validation error (e.g., empty code)
- **500 Internal Server Error**: Server-side analysis failure

Error response format:

```json
{
  "detail": "Error description"
}
```

## Usage Examples

### Example 1: Analyze Python Code

```bash
curl -X POST "http://localhost:8000/api/analysis/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def hello(name):\n    print(f\"Hello, {name}!\")",
    "language": "python",
    "file_name": "greeting.py"
  }'
```

### Example 2: Check Code Quality

```bash
curl -X POST "http://localhost:8000/api/analysis/analyze/quality" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "x = 1\ny = 2\nz = x + y",
    "language": "python"
  }'
```

### Example 3: Detect Issues in JavaScript

```bash
curl -X POST "http://localhost:8000/api/analysis/analyze/issues" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "function process(data) {\n    if (data) {\n        if (data.items) {\n            return data.items;\n        }\n    }\n}",
    "language": "javascript"
  }'
```

### Example 4: Get Debugging Insights

```bash
curl -X POST "http://localhost:8000/api/analysis/analyze/debug" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "while(true) {\n    data = fetch(url);\n}",
    "language": "javascript"
  }'
```

## Performance Considerations

- Analysis duration varies based on code size and complexity
- Typical analysis completes in 10-100ms for small to medium files
- Large files (>10,000 lines) may take 500ms-2s
- Use specific analysis endpoints for faster results when full analysis not needed

## Limitations

- Pattern detection is heuristic-based and may have false positives
- Complex architectural patterns may not be detected
- Language-specific features are simplified for cross-language consistency
- Cannot execute code or analyze dynamic behavior
- Regular expression-based parsing has limitations for edge cases

## Future Enhancements

- Tree-sitter integration for more accurate parsing
- LLM-powered analysis for deeper insights
- Historical analysis tracking and trends
- Custom analysis rule definition
- Integration with popular linters (ESLint, Pylint, etc.)
- Machine learning models for pattern detection
- Code smell detection improvements
- Performance profiling integration

## Testing

The API includes comprehensive test coverage:

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_analysis_api.py
pytest tests/test_analysis_service.py

# Run with coverage
pytest --cov=app tests/
```

## License

MIT License - See LICENSE file for details
