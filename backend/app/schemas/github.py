"""Pydantic schemas for GitHub API"""
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, HttpUrl


class GitHubUserBase(BaseModel):
    """Base GitHub user schema"""

    username: str
    email: Optional[str] = None
    avatar_url: Optional[str] = None


class GitHubUserCreate(GitHubUserBase):
    """Create GitHub user schema"""

    user_id: int
    encrypted_token: str
    token_expires_at: Optional[datetime] = None


class GitHubUserUpdate(BaseModel):
    """Update GitHub user schema"""

    email: Optional[str] = None
    avatar_url: Optional[str] = None


class GitHubUserResponse(GitHubUserBase):
    """GitHub user response schema"""

    id: int
    user_id: int
    last_synced_at: Optional[datetime] = None
    sync_status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class GitHubRepositoryBase(BaseModel):
    """Base GitHub repository schema"""

    repo_name: str
    repo_full_name: str
    repo_url: str
    description: Optional[str] = None
    is_private: bool = False


class GitHubRepositoryCreate(GitHubRepositoryBase):
    """Create GitHub repository schema"""

    repo_id: int


class GitHubRepositoryUpdate(BaseModel):
    """Update GitHub repository schema"""

    selected_for_sync: Optional[bool] = None
    sync_status: Optional[str] = None


class GitHubRepositoryResponse(GitHubRepositoryBase):
    """GitHub repository response schema"""

    id: int
    repo_id: int
    selected_for_sync: bool
    mirror_path: Optional[str] = None
    last_synced_at: Optional[datetime] = None
    sync_status: str
    webhook_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class GitHubOAuthStart(BaseModel):
    """OAuth flow start request"""

    redirect_uri: str


class GitHubOAuthCallback(BaseModel):
    """OAuth callback with authorization code"""

    code: str
    state: Optional[str] = None


class GitHubTokenResponse(BaseModel):
    """GitHub token response"""

    access_token: str
    token_type: str = "bearer"
    scope: str = ""


class RepositoryListResponse(BaseModel):
    """List of repositories response"""

    total_count: int
    repositories: List[GitHubRepositoryResponse]


class SyncStatusResponse(BaseModel):
    """Repository sync status response"""

    status: str
    last_synced_at: Optional[datetime] = None
    message: Optional[str] = None


class FileTreeNode(BaseModel):
    """File tree node for repository"""

    path: str
    type: str  # "file" or "directory"
    size: Optional[int] = None
    children: Optional[List["FileTreeNode"]] = None

    class Config:
        from_attributes = True


FileTreeNode.model_rebuild()


class FileTreeResponse(BaseModel):
    """File tree response"""

    root: FileTreeNode
    total_files: int
    total_size: int


class CodeInspectionRequest(BaseModel):
    """Code inspection request"""

    file_path: str
    repo_id: int


class CodeInspectionResponse(BaseModel):
    """Code inspection response"""

    file_path: str
    content: str
    language: Optional[str] = None
    size: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
