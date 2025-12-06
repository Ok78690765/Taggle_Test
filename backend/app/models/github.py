"""GitHub OAuth and repository models"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.models.base import BaseModel


class GitHubUser(BaseModel):
    """GitHub user OAuth information"""

    __tablename__ = "github_users"

    user_id = Column(Integer, unique=True, nullable=False, index=True)
    username = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), nullable=True)
    avatar_url = Column(String(512), nullable=True)
    encrypted_token = Column(Text, nullable=False)
    token_expires_at = Column(DateTime, nullable=True)
    last_synced_at = Column(DateTime, nullable=True)
    sync_status = Column(String(50), default="pending")

    repositories = relationship("GitHubRepository", back_populates="user")

    def __repr__(self):
        return f"<GitHubUser(id={self.id}, username={self.username})>"


class GitHubRepository(BaseModel):
    """GitHub repository mirror information"""

    __tablename__ = "github_repositories"

    github_user_id = Column(Integer, ForeignKey("github_users.id"), nullable=False)
    repo_id = Column(Integer, nullable=False, index=True)
    repo_name = Column(String(255), nullable=False)
    repo_full_name = Column(String(512), nullable=False, unique=True, index=True)
    repo_url = Column(String(512), nullable=False)
    description = Column(Text, nullable=True)
    is_private = Column(Boolean, default=False)
    mirror_path = Column(String(512), nullable=True)
    selected_for_sync = Column(Boolean, default=False, index=True)
    last_synced_at = Column(DateTime, nullable=True)
    sync_status = Column(String(50), default="pending")
    webhook_id = Column(String(255), nullable=True)

    user = relationship("GitHubUser", back_populates="repositories")

    def __repr__(self):
        return f"<GitHubRepository(id={self.id}, repo_name={self.repo_name})>"


class SyncLog(BaseModel):
    """Repository sync operation log"""

    __tablename__ = "sync_logs"

    github_repository_id = Column(
        Integer, ForeignKey("github_repositories.id"), nullable=False, index=True
    )
    sync_type = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False)
    message = Column(Text, nullable=True)
    files_changed = Column(Integer, default=0)

    def __repr__(self):
        return f"<SyncLog(id={self.id}, status={self.status})>"
