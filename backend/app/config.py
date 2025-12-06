"""Application configuration management"""

from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings from environment variables"""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )

    debug: bool = False
    app_name: str = "FastAPI Backend"
    app_version: str = "0.1.0"

    # Server
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000

    # Database
    database_url: str = "sqlite:///./test.db"

    # CORS
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    # Security
    secret_key: str = "your-secret-key-here-change-in-production"

    # Logging
    log_level: str = "INFO"

    # LLM Providers
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None

    # Repo settings
    repo_root: str = "/home/engine/project"


settings = Settings()
