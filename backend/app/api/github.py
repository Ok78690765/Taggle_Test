"""GitHub OAuth and repository API endpoints"""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.schemas.github import (
    GitHubOAuthCallback,
    GitHubUserResponse,
    RepositoryListResponse,
    GitHubRepositoryResponse,
    SyncStatusResponse,
    CodeInspectionRequest,
    CodeInspectionResponse,
    FileTreeResponse,
)
from app.services.github import (
    GitHubAPIService,
    GitHubUserService,
    RepositoryService,
    RepositorySyncService,
)

router = APIRouter(prefix="/api/github", tags=["github"])

github_api = GitHubAPIService()
repo_sync = RepositorySyncService()


@router.post("/auth/callback")
async def github_oauth_callback(
    request: GitHubOAuthCallback, db: Session = Depends(get_db)
) -> dict:
    """Handle GitHub OAuth callback"""
    try:
        token_response = await github_api.get_access_token(request.code)

        if "error" in token_response:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=token_response.get("error_description", "OAuth failed"),
            )

        access_token = token_response.get("access_token")
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No access token received",
            )

        user_info = await github_api.get_user_info(access_token)

        existing_user = GitHubUserService.get_github_user(db, user_info["login"])
        if existing_user:
            db_user = existing_user
        else:
            db_user = GitHubUserService.create_github_user(
                db,
                user_id=user_info["id"],
                username=user_info["login"],
                token=access_token,
                email=user_info.get("email"),
                avatar_url=user_info.get("avatar_url"),
            )

        return {
            "success": True,
            "user_id": db_user.id,
            "username": db_user.username,
            "message": "Authentication successful",
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Authentication failed: {str(e)}",
        )


@router.get("/auth/oauth-url")
async def get_oauth_url() -> dict:
    """Get GitHub OAuth URL for frontend redirect"""
    if not settings.github_client_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="GitHub OAuth not configured",
        )

    oauth_url = (
        f"https://github.com/login/oauth/authorize"
        f"?client_id={settings.github_client_id}"
        f"&redirect_uri={settings.github_redirect_uri}"
        f"&scope=repo,user"
        f"&allow_signup=true"
    )

    return {"oauth_url": oauth_url}


@router.get("/user/{user_id}", response_model=GitHubUserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get authenticated GitHub user info"""
    user = GitHubUserService.get_github_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.post("/repositories/sync/{user_id}")
async def sync_repositories(user_id: int, db: Session = Depends(get_db)) -> dict:
    """Sync repositories for a user"""
    user = GitHubUserService.get_github_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    try:
        from app.utils.encryption import token_encryption

        decrypted_token = token_encryption.decrypt(user.encrypted_token)
        repos_data = await github_api.list_repositories(decrypted_token)

        created_count = 0
        for repo_data in repos_data:
            existing = RepositoryService.get_repository_by_full_name(
                db, repo_data["full_name"]
            )
            if not existing:
                RepositoryService.create_repository(db, user.id, repo_data)
                created_count += 1

        GitHubUserService.update_last_sync(db, user.id)

        return {
            "success": True,
            "total_repositories": len(repos_data),
            "new_repositories": created_count,
            "message": "Repository sync completed",
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to sync repositories: {str(e)}",
        )


@router.get("/repositories/{user_id}", response_model=RepositoryListResponse)
async def list_repositories(
    user_id: int, selected_only: bool = False, db: Session = Depends(get_db)
):
    """List repositories for a user"""
    user = GitHubUserService.get_github_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if selected_only:
        repos = RepositoryService.list_selected_repositories(db, user.id)
    else:
        repos = RepositoryService.list_user_repositories(db, user.id)

    return RepositoryListResponse(
        total_count=len(repos),
        repositories=repos,
    )


@router.put("/repositories/{repo_id}/select")
async def toggle_repository_selection(
    repo_id: int, selected: bool, db: Session = Depends(get_db)
) -> dict:
    """Toggle repository selection for sync"""
    repo = RepositoryService.update_repository_selection(db, repo_id, selected)
    if not repo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Repository not found"
        )

    return {
        "success": True,
        "repo_id": repo.id,
        "selected": repo.selected_for_sync,
        "message": "Repository selection updated",
    }


@router.post("/repositories/{repo_id}/clone", response_model=SyncStatusResponse)
async def clone_repository(
    repo_id: int, db: Session = Depends(get_db)
):
    """Clone/mirror a repository"""
    repo = RepositoryService.get_repository(db, repo_id)
    if not repo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Repository not found"
        )

    user = GitHubUserService.get_github_user_by_id(db, repo.github_user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    try:
        from app.utils.encryption import token_encryption

        decrypted_token = token_encryption.decrypt(user.encrypted_token)
        mirror_path = repo_sync.get_mirror_path(repo.repo_full_name)

        RepositoryService.update_repository_sync_status(
            db, repo_id, "cloning", mirror_path
        )

        success = repo_sync.clone_repository(
            repo.repo_url, mirror_path, decrypted_token
        )
        if success:
            RepositoryService.update_repository_sync_status(db, repo_id, "synced")
            return SyncStatusResponse(
                status="synced",
                last_synced_at=repo.last_synced_at,
                message="Repository cloned successfully",
            )
        else:
            RepositoryService.update_repository_sync_status(db, repo_id, "failed")
            return SyncStatusResponse(
                status="failed", message="Failed to clone repository"
            )
    except Exception as e:
        RepositoryService.update_repository_sync_status(db, repo_id, "failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Clone operation failed: {str(e)}",
        )


@router.post("/repositories/{repo_id}/update", response_model=SyncStatusResponse)
async def update_repository(
    repo_id: int, db: Session = Depends(get_db)
):
    """Update an existing repository mirror"""
    repo = RepositoryService.get_repository(db, repo_id)
    if not repo or not repo.mirror_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Repository not found"
        )

    try:
        RepositoryService.update_repository_sync_status(
            db, repo_id, "updating", repo.mirror_path
        )

        success = repo_sync.update_repository(repo.mirror_path)
        if success:
            RepositoryService.update_repository_sync_status(db, repo_id, "synced")
            return SyncStatusResponse(
                status="synced",
                last_synced_at=repo.last_synced_at,
                message="Repository updated successfully",
            )
        else:
            RepositoryService.update_repository_sync_status(db, repo_id, "failed")
            return SyncStatusResponse(
                status="failed", message="Failed to update repository"
            )
    except Exception as e:
        RepositoryService.update_repository_sync_status(db, repo_id, "failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Update operation failed: {str(e)}",
        )


@router.get("/repositories/{repo_id}/status", response_model=SyncStatusResponse)
async def get_repository_sync_status(
    repo_id: int, db: Session = Depends(get_db)
):
    """Get repository sync status"""
    repo = RepositoryService.get_repository(db, repo_id)
    if not repo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Repository not found"
        )

    return SyncStatusResponse(
        status=repo.sync_status,
        last_synced_at=repo.last_synced_at,
        message=f"Status: {repo.sync_status}",
    )


@router.get("/repositories/{repo_id}/files", response_model=FileTreeResponse)
async def get_repository_file_tree(
    repo_id: int, db: Session = Depends(get_db)
):
    """Get file tree for a repository"""
    repo = RepositoryService.get_repository(db, repo_id)
    if not repo or not repo.mirror_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Repository not found"
        )

    try:
        file_tree = repo_sync.get_file_tree(repo.mirror_path)

        def count_files(node: dict) -> int:
            count = 1 if node["type"] == "file" else 0
            if "children" in node:
                count += sum(count_files(child) for child in node["children"])
            return count

        def calc_size(node: dict) -> int:
            size = node.get("size", 0)
            if "children" in node:
                size += sum(calc_size(child) for child in node["children"])
            return size

        total_files = count_files(file_tree) - 1
        total_size = calc_size(file_tree)

        return FileTreeResponse(
            root=file_tree, total_files=total_files, total_size=total_size
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve file tree: {str(e)}",
        )


@router.post("/repositories/{repo_id}/inspect", response_model=CodeInspectionResponse)
async def inspect_code_file(
    repo_id: int, request: CodeInspectionRequest, db: Session = Depends(get_db)
):
    """Retrieve file content for code inspection"""
    repo = RepositoryService.get_repository(db, repo_id)
    if not repo or not repo.mirror_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Repository not found"
        )

    try:
        result = repo_sync.read_file(repo.mirror_path, request.file_path)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
            )

        content, size = result

        return CodeInspectionResponse(
            file_path=request.file_path, content=content, size=size
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to inspect file: {str(e)}",
        )


@router.post("/repositories/{repo_id}/webhook")
async def create_repository_webhook(
    repo_id: int, db: Session = Depends(get_db)
) -> dict:
    """Create webhook for repository push events"""
    repo = RepositoryService.get_repository(db, repo_id)
    if not repo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Repository not found"
        )

    user = GitHubUserService.get_github_user_by_id(db, repo.github_user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    try:
        from app.utils.encryption import token_encryption

        decrypted_token = token_encryption.decrypt(user.encrypted_token)
        owner, repo_name = repo.repo_full_name.split("/")
        callback_url = f"{settings.backend_url}/api/github/webhook/push"

        webhook = await github_api.create_webhook(
            decrypted_token, owner, repo_name, callback_url
        )
        if webhook:
            return {"success": True, "webhook_id": webhook.get("id")}
        else:
            return {"success": False, "message": "Failed to create webhook"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create webhook: {str(e)}",
        )


@router.post("/webhook/push")
async def handle_push_webhook(payload: dict, db: Session = Depends(get_db)) -> dict:
    """Handle GitHub push webhook"""
    try:
        repo_full_name = payload.get("repository", {}).get("full_name")
        if not repo_full_name:
            return {"success": False, "message": "Invalid webhook payload"}

        repo = RepositoryService.get_repository_by_full_name(db, repo_full_name)
        if not repo or not repo.mirror_path:
            return {"success": False, "message": "Repository not found"}

        success = repo_sync.update_repository(repo.mirror_path)
        if success:
            RepositoryService.update_repository_sync_status(db, repo.id, "synced")
            return {"success": True, "message": "Repository updated via webhook"}
        else:
            return {"success": False, "message": "Failed to update repository"}
    except Exception as e:
        return {"success": False, "message": f"Webhook processing failed: {str(e)}"}
