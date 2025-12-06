"""Application configuration management"""
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings from environment variables"""

    debug: bool = False
    app_name: str = "FastAPI Backend"
    app_version: str = "0.1.0"

    # Server
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    backend_url: str = "http://localhost:8000"

    # Database
    database_url: str = "sqlite:///./test.db"

    # CORS
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    # Security
    secret_key: str = "your-secret-key-here-change-in-production-min-32"

    # Logging
    log_level: str = "INFO"

    # GitHub OAuth
    github_client_id: str = ""
    github_client_secret: str = ""
    github_redirect_uri: str = "http://localhost:3000/auth/github/callback"

    # Session
    session_secret_key: str = "session-secret-key-change-in-production-min-32"

    # Repository storage
    repos_mirror_path: str = "/tmp/github_mirrors"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
