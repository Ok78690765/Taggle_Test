"""GitHub API integration service"""
import os
import shutil
from datetime import datetime
from typing import Optional, List
import subprocess

import httpx
from sqlalchemy.orm import Session

from app.config import settings
from app.models import GitHubUser, GitHubRepository, SyncLog
from app.schemas.github import GitHubRepositoryResponse
from app.utils.encryption import token_encryption


class GitHubAPIService:
    """GitHub API service for OAuth and repository operations"""

    BASE_URL = "https://api.github.com"

    def __init__(self):
        self.client_id = settings.github_client_id
        self.client_secret = settings.github_client_secret

    async def get_access_token(self, code: str) -> dict:
        """Exchange authorization code for access token"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://github.com/login/oauth/access_token",
                params={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "code": code,
                },
                headers={"Accept": "application/json"},
            )
            response.raise_for_status()
            return response.json()

    async def get_user_info(self, token: str) -> dict:
        """Get authenticated user information"""
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3+json",
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.BASE_URL}/user", headers=headers)
            response.raise_for_status()
            return response.json()

    async def list_repositories(self, token: str) -> List[dict]:
        """List all repositories for authenticated user"""
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3+json",
        }
        repos = []
        page = 1

        async with httpx.AsyncClient() as client:
            while True:
                response = await client.get(
                    f"{self.BASE_URL}/user/repos",
                    headers=headers,
                    params={"page": page, "per_page": 100},
                )
                response.raise_for_status()
                data = response.json()

                if not data:
                    break

                repos.extend(data)
                page += 1

        return repos

    async def create_webhook(
        self, token: str, owner: str, repo: str, callback_url: str
    ) -> Optional[dict]:
        """Create a webhook for repository push events"""
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3+json",
        }
        payload = {
            "name": "web",
            "active": True,
            "events": ["push", "pull_request"],
            "config": {"url": callback_url, "content_type": "json"},
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/repos/{owner}/{repo}/hooks",
                headers=headers,
                json=payload,
            )
            if response.status_code == 201:
                return response.json()
            return None

    async def delete_webhook(
        self, token: str, owner: str, repo: str, hook_id: str
    ) -> bool:
        """Delete a webhook"""
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3+json",
        }

        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{self.BASE_URL}/repos/{owner}/{repo}/hooks/{hook_id}",
                headers=headers,
            )
            return response.status_code == 204


class RepositorySyncService:
    """Service for synchronizing repository mirrors"""

    def __init__(self):
        self.mirror_base_path = settings.repos_mirror_path
        os.makedirs(self.mirror_base_path, exist_ok=True)

    def get_mirror_path(self, repo_full_name: str) -> str:
        """Get local mirror path for repository"""
        return os.path.join(self.mirror_base_path, repo_full_name.replace("/", "_"))

    def clone_repository(self, repo_url: str, local_path: str, token: str) -> bool:
        """Clone repository with authentication"""
        try:
            url_with_token = repo_url.replace(
                "https://", f"https://x-access-token:{token}@"
            )
            subprocess.run(
                ["git", "clone", "--mirror", url_with_token, local_path],
                check=True,
                capture_output=True,
                timeout=300,
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to clone repository: {e.stderr.decode()}")
            return False
        except Exception as e:
            print(f"Error cloning repository: {str(e)}")
            return False

    def update_repository(self, local_path: str) -> bool:
        """Update existing mirror repository"""
        try:
            subprocess.run(
                ["git", "fetch", "--all"],
                cwd=local_path,
                check=True,
                capture_output=True,
                timeout=300,
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to update repository: {e.stderr.decode()}")
            return False
        except Exception as e:
            print(f"Error updating repository: {str(e)}")
            return False

    def get_file_tree(self, local_path: str, prefix: str = "") -> dict:
        """Build file tree from repository"""
        tree = {"path": prefix or "/", "type": "directory", "children": []}

        if not os.path.exists(local_path):
            return tree

        try:
            entries = sorted(os.listdir(local_path))
            for entry in entries:
                if entry.startswith("."):
                    continue

                entry_path = os.path.join(local_path, entry)
                relative_path = f"{prefix}/{entry}" if prefix else f"/{entry}"

                if os.path.isdir(entry_path):
                    subtree = self.get_file_tree(entry_path, relative_path)
                    tree["children"].append(subtree)
                else:
                    size = os.path.getsize(entry_path)
                    tree["children"].append(
                        {"path": relative_path, "type": "file", "size": size}
                    )
        except Exception as e:
            print(f"Error building file tree: {str(e)}")

        return tree

    def read_file(
        self, local_path: str, file_path: str
    ) -> Optional[tuple[str, int]]:
        """Read file from repository"""
        try:
            full_path = os.path.join(local_path, file_path.lstrip("/"))
            if not os.path.isfile(full_path):
                return None

            with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                size = len(content.encode("utf-8"))
                return content, size
        except Exception as e:
            print(f"Error reading file: {str(e)}")
            return None

    def delete_repository(self, local_path: str) -> bool:
        """Delete repository mirror"""
        try:
            if os.path.exists(local_path):
                shutil.rmtree(local_path)
            return True
        except Exception as e:
            print(f"Error deleting repository: {str(e)}")
            return False


class GitHubUserService:
    """Service for managing GitHub user data"""

    @staticmethod
    def create_github_user(
        db: Session, user_id: int, username: str, token: str, **kwargs
    ) -> GitHubUser:
        """Create new GitHub user record"""
        encrypted_token = token_encryption.encrypt(token)
        db_user = GitHubUser(
            user_id=user_id,
            username=username,
            encrypted_token=encrypted_token,
            email=kwargs.get("email"),
            avatar_url=kwargs.get("avatar_url"),
            sync_status="pending",
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_github_user(db: Session, username: str) -> Optional[GitHubUser]:
        """Get GitHub user by username"""
        return db.query(GitHubUser).filter(GitHubUser.username == username).first()

    @staticmethod
    def get_github_user_by_id(db: Session, user_id: int) -> Optional[GitHubUser]:
        """Get GitHub user by ID"""
        return db.query(GitHubUser).filter(GitHubUser.id == user_id).first()

    @staticmethod
    def update_last_sync(db: Session, user_id: int) -> None:
        """Update last sync timestamp"""
        user = db.query(GitHubUser).filter(GitHubUser.id == user_id).first()
        if user:
            user.last_synced_at = datetime.utcnow()
            db.commit()


class RepositoryService:
    """Service for managing repository records"""

    @staticmethod
    def create_repository(
        db: Session, github_user_id: int, repo_data: dict
    ) -> GitHubRepository:
        """Create new repository record"""
        db_repo = GitHubRepository(
            github_user_id=github_user_id,
            repo_id=repo_data["id"],
            repo_name=repo_data["name"],
            repo_full_name=repo_data["full_name"],
            repo_url=repo_data["clone_url"],
            description=repo_data.get("description"),
            is_private=repo_data.get("private", False),
            sync_status="pending",
        )
        db.add(db_repo)
        db.commit()
        db.refresh(db_repo)
        return db_repo

    @staticmethod
    def list_user_repositories(
        db: Session, github_user_id: int
    ) -> List[GitHubRepository]:
        """List all repositories for a user"""
        return (
            db.query(GitHubRepository)
            .filter(GitHubRepository.github_user_id == github_user_id)
            .all()
        )

    @staticmethod
    def list_selected_repositories(
        db: Session, github_user_id: int
    ) -> List[GitHubRepository]:
        """List selected repositories for sync"""
        return (
            db.query(GitHubRepository)
            .filter(
                GitHubRepository.github_user_id == github_user_id,
                GitHubRepository.selected_for_sync == True,
            )
            .all()
        )

    @staticmethod
    def update_repository_selection(
        db: Session, repo_id: int, selected: bool
    ) -> Optional[GitHubRepository]:
        """Update repository selection status"""
        repo = db.query(GitHubRepository).filter(GitHubRepository.id == repo_id).first()
        if repo:
            repo.selected_for_sync = selected
            db.commit()
            db.refresh(repo)
        return repo

    @staticmethod
    def update_repository_sync_status(
        db: Session, repo_id: int, status: str, mirror_path: Optional[str] = None
    ) -> None:
        """Update repository sync status"""
        repo = db.query(GitHubRepository).filter(GitHubRepository.id == repo_id).first()
        if repo:
            repo.sync_status = status
            repo.last_synced_at = datetime.utcnow()
            if mirror_path:
                repo.mirror_path = mirror_path
            db.commit()

    @staticmethod
    def get_repository(db: Session, repo_id: int) -> Optional[GitHubRepository]:
        """Get repository by ID"""
        return (
            db.query(GitHubRepository).filter(GitHubRepository.id == repo_id).first()
        )

    @staticmethod
    def get_repository_by_full_name(
        db: Session, full_name: str
    ) -> Optional[GitHubRepository]:
        """Get repository by full name"""
        return (
            db.query(GitHubRepository)
            .filter(GitHubRepository.repo_full_name == full_name)
            .first()
        )
