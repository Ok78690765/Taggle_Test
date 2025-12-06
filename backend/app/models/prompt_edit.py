"""Domain models for prompt-based code editing"""

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class EditSession(Base):
    """Model for tracking code editing sessions"""

    __tablename__ = "edit_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(255), unique=True, index=True, nullable=False)
    user_prompt = Column(Text, nullable=False)
    repo_context = Column(JSON, nullable=True)
    status = Column(String(50), nullable=False, default="pending")
    llm_provider = Column(String(50), nullable=False, default="mock")
    llm_model = Column(String(255), nullable=True)
    dry_run = Column(Boolean, nullable=False, default=True)
    validation_status = Column(String(50), nullable=False, default="pending")
    formatting_status = Column(String(50), nullable=False, default="pending")
    test_status = Column(String(50), nullable=False, default="pending")
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    edits = relationship("CodeEdit", back_populates="session", cascade="all, delete")
    validations = relationship(
        "EditValidation", back_populates="session", cascade="all, delete"
    )


class CodeEdit(Base):
    """Model for storing individual code edit plans"""

    __tablename__ = "code_edits"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(
        String(255),
        ForeignKey("edit_sessions.session_id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    file_path = Column(String(500), nullable=False)
    original_content = Column(Text, nullable=True)
    modified_content = Column(Text, nullable=True)
    edit_type = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    applied = Column(Boolean, default=False, nullable=False)
    validated = Column(Boolean, default=False, nullable=False)
    formatted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    session = relationship("EditSession", back_populates="edits")


class EditValidation(Base):
    """Model for storing validation results"""

    __tablename__ = "edit_validations"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(
        String(255),
        ForeignKey("edit_sessions.session_id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    validation_type = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False)
    message = Column(Text, nullable=True)
    details = Column(JSON, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    session = relationship("EditSession", back_populates="validations")
