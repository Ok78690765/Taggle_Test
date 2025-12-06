"""Domain models for code analysis"""

from sqlalchemy import Column, Float, Integer, String, Text

from app.database import Base


class CodeAnalysis(Base):
    """Model for storing code analysis results"""

    __tablename__ = "code_analysis"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(255), nullable=False)
    language = Column(String(50), nullable=False)
    code_content = Column(Text, nullable=False)

    quality_score = Column(Float, nullable=True)
    complexity_score = Column(Float, nullable=True)
    maintainability_index = Column(Float, nullable=True)

    created_at = Column(String, nullable=False)
    updated_at = Column(String, nullable=False)


class AnalysisIssue(Base):
    """Model for storing detected issues"""

    __tablename__ = "analysis_issues"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, nullable=False)
    issue_type = Column(String(50), nullable=False)
    severity = Column(String(20), nullable=False)
    line_number = Column(Integer, nullable=True)
    column_number = Column(Integer, nullable=True)
    message = Column(Text, nullable=False)
    suggestion = Column(Text, nullable=True)

    created_at = Column(String, nullable=False)
