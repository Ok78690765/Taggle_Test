"""Application configuration management"""

import secrets
from typing import Optional, List, Union

from pydantic import field_validator, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings from environment variables"""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_prefix="",
    )

    # Application settings
    app_name: str = "FastAPI Backend"
    app_version: str = "0.1.0"
    
    # Environment configuration
    debug: bool = False
    environment: str = "development"

    # Server configuration
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    
    # Alternative port variable (for platforms like Railway/Heroku)
    port: Optional[int] = None

    # Database
    database_url: str = "sqlite:///./test.db"

    # CORS configuration - flexible format handling  
    cors_origins: Union[str, List[str]] = "http://localhost:3000,http://localhost:5173"

    # Security
    secret_key: str = Field(default_factory=lambda: secrets.token_urlsafe(32))
    api_key: Optional[str] = None

    # GitHub integration (optional)
    github_token: Optional[str] = None

    # Logging
    log_level: str = "INFO"

    # Feature flags
    enable_api_docs: bool = True

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        """Parse CORS origins from comma-separated string or list"""
        if isinstance(v, str):
            # Split by comma and strip whitespace
            origins = [origin.strip() for origin in v.split(",") if origin.strip()]
            return origins if origins else ["http://localhost:3000"]
        elif isinstance(v, list):
            return v
        elif v is None:
            return ["http://localhost:3000"]
        else:
            return ["http://localhost:3000"]

    @field_validator("backend_port", "port", mode="before")
    @classmethod
    def parse_port(cls, v: Optional[Union[str, int]]) -> Optional[int]:
        """Parse port from string to int"""
        if v is None:
            return None
        if isinstance(v, str) and v.isdigit():
            return int(v)
        return v

    @property
    def final_port(self) -> int:
        """Get the final port to use, prioritizing port over backend_port"""
        return self.port if self.port is not None else self.backend_port

    @field_validator("environment")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Validate environment value"""
        valid_environments = ["development", "staging", "production"]
        if v.lower() not in valid_environments:
            raise ValueError(f"Environment must be one of: {valid_environments}")
        return v.lower()

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level"""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of: {valid_levels}")
        return v.upper()

    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        """Ensure secret key is not the default placeholder"""
        if v == "your-secret-key-here-change-in-production":
            # Generate a secure random key if the default is used
            return secrets.token_urlsafe(32)
        return v


settings = Settings()
