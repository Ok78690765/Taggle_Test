"""API endpoints for code analysis"""

from fastapi import APIRouter, HTTPException

from app.schemas.analysis import (
    CodeAnalysisRequestSchema,
    CodeAnalysisResponseSchema,
    DebugAnalysisResponseSchema,
)
from app.services.code_analyzer import AnalysisService

router = APIRouter(prefix="/api/analysis", tags=["analysis"])

analysis_service = AnalysisService()


@router.post(
    "/analyze",
    response_model=CodeAnalysisResponseSchema,
    summary="Analyze code for quality, issues, and insights",
    description="Performs comprehensive code analysis including quality scoring, issue detection, architecture insights, and formatting recommendations",
)
async def analyze_code(
    request: CodeAnalysisRequestSchema,
) -> CodeAnalysisResponseSchema:
    """
    Analyze code for quality, debugging issues, architecture insights, and formatting.

    This endpoint performs a comprehensive analysis of the provided code and returns:
    - Quality scores (overall, code quality, maintainability, complexity, duplication)
    - Detected issues (style, complexity, naming)
    - Complexity metrics (cyclomatic, cognitive, nesting depth)
    - Architecture insights (design patterns detected)
    - Formatting recommendations

    **Parameters:**
    - `code`: Source code to analyze (required)
    - `language`: Programming language (python, javascript, typescript, java, etc.)
    - `file_name`: Optional file name for context
    - `analyze_*`: Flags to enable/disable specific analyses

    **Supported Languages:**
    - Python (python, py)
    - JavaScript (javascript, js)
    - TypeScript (typescript, ts)
    - Java (java)

    **Returns:**
    - Complete analysis results including scores, issues, metrics, insights, and recommendations
    """
    try:
        result = analysis_service.analyze_full(
            code=request.code,
            language=request.language,
            file_name=request.file_name,
        )

        return CodeAnalysisResponseSchema(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post(
    "/analyze/quality",
    summary="Analyze code quality score",
    description="Returns a quality score assessment of the provided code",
)
async def analyze_quality(request: CodeAnalysisRequestSchema):
    """
    Analyze code quality score.

    Returns a quality score with ratings for:
    - Overall score (0-100)
    - Code quality (0-100)
    - Maintainability (0-100)
    - Complexity assessment (0-100, lower is better)
    - Duplication score (0-100)
    """
    try:
        from app.services.code_analyzer import CodeAnalyzer

        analyzer = CodeAnalyzer()
        quality_score = analyzer.analyze_quality(request.code, request.language)

        return {
            "file_name": request.file_name,
            "language": request.language,
            "quality_score": quality_score,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post(
    "/analyze/issues",
    summary="Detect issues in code",
    description="Detects style, complexity, and naming issues in the provided code",
)
async def analyze_issues(request: CodeAnalysisRequestSchema):
    """
    Detect issues in code.

    Returns a list of detected issues including:
    - Style issues (line length, formatting)
    - Complexity issues (high complexity, deep nesting)
    - Naming issues (single-letter variables, conventions)

    Each issue includes:
    - Type and severity
    - Line and column numbers
    - Human-readable message
    - Suggested fix
    """
    try:
        from app.services.code_analyzer import CodeAnalyzer

        analyzer = CodeAnalyzer()
        issues = analyzer.analyze_issues(request.code, request.language)

        return {
            "file_name": request.file_name,
            "language": request.language,
            "issues": issues,
            "total_issues": len(issues),
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post(
    "/analyze/complexity",
    summary="Analyze code complexity metrics",
    description="Calculates complexity metrics for the provided code",
)
async def analyze_complexity(request: CodeAnalysisRequestSchema):
    """
    Analyze code complexity metrics.

    Returns complexity metrics including:
    - Cyclomatic complexity (how many independent paths through code)
    - Cognitive complexity (how difficult to understand)
    - Lines of code
    - Maximum nesting depth
    """
    try:
        from app.services.code_analyzer import CodeAnalyzer

        analyzer = CodeAnalyzer()
        complexity = analyzer.analyze_complexity(request.code, request.language)

        return {
            "file_name": request.file_name,
            "language": request.language,
            "complexity_metrics": complexity,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post(
    "/analyze/architecture",
    summary="Analyze architectural patterns and insights",
    description="Detects design patterns and architectural issues in the provided code",
)
async def analyze_architecture(request: CodeAnalysisRequestSchema):
    """
    Analyze architectural patterns and insights.

    Returns detected architectural patterns including:
    - Design patterns (Singleton, Factory, Observer, etc.)
    - Layering issues (mixed concerns)
    - Architectural recommendations

    Each insight includes:
    - Pattern name and confidence level
    - Description
    - Recommendations for improvement
    """
    try:
        from app.services.code_analyzer import CodeAnalyzer

        analyzer = CodeAnalyzer()
        insights = analyzer.analyze_architecture(request.code, request.language)

        return {
            "file_name": request.file_name,
            "language": request.language,
            "architecture_insights": insights,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post(
    "/analyze/formatting",
    summary="Get formatting recommendations",
    description="Provides formatting and style recommendations for the provided code",
)
async def analyze_formatting(request: CodeAnalysisRequestSchema):
    """
    Get formatting and style recommendations.

    Returns formatting recommendations for:
    - Indentation style
    - Semicolon usage
    - Brace placement
    - Line length
    - Other language-specific conventions

    Each recommendation includes:
    - Current vs. recommended style
    - Reason for recommendation
    - Affected line numbers
    """
    try:
        from app.services.code_analyzer import CodeAnalyzer

        analyzer = CodeAnalyzer()
        recommendations = analyzer.analyze_formatting(request.code, request.language)

        return {
            "file_name": request.file_name,
            "language": request.language,
            "formatting_recommendations": recommendations,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post(
    "/analyze/debug",
    response_model=DebugAnalysisResponseSchema,
    summary="Analyze code for debugging insights",
    description="Provides debugging and issue detection analysis",
)
async def analyze_for_debugging(
    request: CodeAnalysisRequestSchema,
) -> DebugAnalysisResponseSchema:
    """
    Analyze code for debugging and issue detection.

    Returns debugging insights including:
    - Potential runtime issues
    - Resource leak risks
    - Null pointer/undefined reference risks
    - Infinite loop detection
    - Uninitialized variable detection
    - Common issues found in the code

    Each insight includes:
    - Issue description and severity
    - Affected code areas
    - Debugging steps to investigate
    - Related line numbers
    """
    try:
        result = analysis_service.analyze_for_debugging(
            code=request.code,
            language=request.language,
            file_name=request.file_name,
        )

        return DebugAnalysisResponseSchema(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.get(
    "/supported-languages",
    summary="Get supported languages",
    description="Returns list of supported programming languages",
)
async def get_supported_languages():
    """
    Get list of supported programming languages for analysis.

    Returns a list of language codes that can be analyzed by the API.
    """
    from app.utils.language_adapter import LanguageAdapterFactory

    factory = LanguageAdapterFactory()
    return {
        "supported_languages": factory.supported_languages(),
        "count": len(factory.supported_languages()),
    }
