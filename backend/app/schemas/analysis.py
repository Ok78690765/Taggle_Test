"""Schemas for code analysis API"""

from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema


class IssueSchema(BaseSchema):
    """Schema for a single code issue"""

    issue_type: str = Field(
        ..., description="Type of issue (e.g., complexity, lint, style)"
    )
    severity: str = Field(..., description="Severity level (error, warning, info)")
    line_number: Optional[int] = Field(
        None, description="Line number where issue occurs"
    )
    column_number: Optional[int] = Field(
        None, description="Column number where issue occurs"
    )
    message: str = Field(..., description="Human-readable issue description")
    suggestion: Optional[str] = Field(None, description="Suggested fix or improvement")


class ComplexityMetricsSchema(BaseSchema):
    """Schema for complexity metrics"""

    cyclomatic_complexity: float = Field(..., description="Cyclomatic complexity score")
    cognitive_complexity: float = Field(..., description="Cognitive complexity score")
    lines_of_code: int = Field(..., description="Total lines of code")
    nesting_depth: int = Field(..., description="Maximum nesting depth")


class QualityScoreSchema(BaseSchema):
    """Schema for overall quality score"""

    overall_score: float = Field(
        ..., ge=0, le=100, description="Overall quality score 0-100"
    )
    code_quality: float = Field(..., ge=0, le=100, description="Code quality rating")
    maintainability: float = Field(
        ..., ge=0, le=100, description="Maintainability rating"
    )
    complexity: float = Field(
        ..., ge=0, le=100, description="Complexity assessment (lower is better)"
    )
    duplication: float = Field(..., ge=0, le=100, description="Code duplication score")


class ArchitectureInsightSchema(BaseSchema):
    """Schema for architecture insights"""

    pattern_detected: str = Field(..., description="Design pattern identified")
    confidence: float = Field(
        ..., ge=0, le=1, description="Confidence level of detection"
    )
    description: str = Field(
        ..., description="Description of the architectural pattern"
    )
    recommendations: list[str] = Field(
        default_factory=list, description="Recommendations for improvement"
    )


class FormattingRecommendationSchema(BaseSchema):
    """Schema for formatting recommendations"""

    category: str = Field(..., description="Category of formatting issue")
    current_style: str = Field(..., description="Current code style")
    recommended_style: str = Field(..., description="Recommended code style")
    reason: str = Field(..., description="Why this change is recommended")
    line_number: Optional[int] = Field(None, description="Line number of the issue")


class CodeAnalysisRequestSchema(BaseModel):
    """Request schema for code analysis"""

    code: str = Field(..., description="Source code to analyze", min_length=1)
    language: str = Field(
        ...,
        description="Programming language (python, javascript, typescript, java, etc.)",
    )
    file_name: Optional[str] = Field(None, description="Optional file name for context")
    analyze_quality: bool = Field(True, description="Include quality scoring")
    analyze_issues: bool = Field(True, description="Include issue detection")
    analyze_architecture: bool = Field(
        True, description="Include architecture insights"
    )
    analyze_formatting: bool = Field(
        True, description="Include formatting recommendations"
    )


class CodeAnalysisResponseSchema(BaseSchema):
    """Response schema for complete code analysis"""

    file_name: Optional[str] = Field(None, description="File name analyzed")
    language: str = Field(..., description="Programming language analyzed")
    code_length: int = Field(..., description="Number of lines in analyzed code")

    quality_score: Optional[QualityScoreSchema] = Field(
        None, description="Quality scores"
    )
    issues: list[IssueSchema] = Field(
        default_factory=list, description="Detected issues"
    )
    complexity_metrics: Optional[ComplexityMetricsSchema] = Field(
        None, description="Complexity metrics"
    )
    architecture_insights: list[ArchitectureInsightSchema] = Field(
        default_factory=list, description="Architectural patterns detected"
    )
    formatting_recommendations: list[FormattingRecommendationSchema] = Field(
        default_factory=list, description="Formatting recommendations"
    )

    analysis_duration_ms: float = Field(
        ..., description="Time taken to analyze in milliseconds"
    )


class DebugInsightSchema(BaseSchema):
    """Schema for debugging insights"""

    potential_issue: str = Field(..., description="Description of potential issue")
    severity: str = Field(..., description="Severity level")
    affected_areas: list[str] = Field(
        default_factory=list, description="Code areas that may be affected"
    )
    debug_steps: list[str] = Field(
        default_factory=list, description="Suggested debugging steps"
    )
    related_line_numbers: list[int] = Field(
        default_factory=list, description="Related line numbers"
    )


class DebugAnalysisResponseSchema(BaseSchema):
    """Response schema for debugging analysis"""

    file_name: Optional[str] = Field(None, description="File name analyzed")
    language: str = Field(..., description="Programming language analyzed")
    debug_insights: list[DebugInsightSchema] = Field(
        default_factory=list, description="Debugging insights"
    )
    common_issues: list[str] = Field(
        default_factory=list, description="Common issues found in the code"
    )
    analysis_duration_ms: float = Field(
        ..., description="Time taken to analyze in milliseconds"
    )
