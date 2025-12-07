"""Application configuration management"""

import os
from typing import Literal, Optional, Union

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings from environment variables"""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )

    # Environment
    environment: Literal["development", "staging", "production"] = "development"

    # App info
    app_name: str = "FastAPI Backend"
    app_version: str = "0.1.0"

    # Debug mode - will be set by model_validator based on environment
    debug: Optional[bool] = None

    # Server
    backend_host: str = "0.0.0.0"
    # PORT is preferred (Railway, Heroku); BACKEND_PORT is fallback
    port: Optional[int] = None
    # Will be set by model_validator based on port preference
    backend_port: int = Field(default=8000, init=False)

    # Database
    database_url: str = "sqlite:///./test.db"

    # CORS - parse from comma-separated string if provided
    cors_origins: Union[str, list[str]] = "http://localhost:3000,http://localhost:5173"

    # Security
    secret_key: str = "your-secret-key-here-change-in-production"

    # Logging - will be set by model_validator based on environment
    log_level: Optional[str] = None

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS origins from comma-separated string or list"""
        if isinstance(v, str):
            # Split by comma and strip whitespace
            origins = [origin.strip() for origin in v.split(",") if origin.strip()]
            return origins
        return v

    @field_validator("environment", mode="before")
    @classmethod
    def validate_environment(cls, v):
        """Ensure environment is lowercase"""
        if isinstance(v, str):
            return v.lower()
        return v

    @model_validator(mode="after")
    def set_defaults_from_environment(self):
        """Set default values based on environment and PORT preference"""
        # Set backend_port: prefer PORT env var (Railway, Heroku) over BACKEND_PORT
        if self.port is not None:
            self.backend_port = self.port
        elif "BACKEND_PORT" in os.environ:
            self.backend_port = int(os.environ["BACKEND_PORT"])
        # else: keep default 8000

        # Set debug based on environment if not explicitly set
        if self.debug is None:
            self.debug = self.environment == "development"

        # Set log_level based on environment if not explicitly set
        if self.log_level is None:
            self.log_level = "DEBUG" if self.environment == "development" else "INFO"

        return self

    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.environment == "production"

    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.environment == "development"


settings = Settings()
