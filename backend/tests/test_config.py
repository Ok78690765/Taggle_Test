"""Tests for configuration module"""

import os
import pytest
from unittest.mock import patch

from app.config import Settings


class TestSettings:
    """Test the Settings configuration class"""

    def test_default_settings(self):
        """Test that default settings load without errors"""
        settings = Settings()
        assert settings.app_name == "FastAPI Backend"
        assert settings.app_version == "0.1.0"
        assert settings.debug is False
        assert settings.environment == "development"
        assert settings.secret_key != "your-secret-key-here-change-in-production"
        assert settings.log_level == "INFO"

    def test_cors_origins_single_url(self):
        """Test CORS origins with single URL"""
        settings = Settings(cors_origins="https://example.com")
        assert settings.cors_origins == ["https://example.com"]

    def test_cors_origins_multiple_urls(self):
        """Test CORS origins with multiple URLs"""
        settings = Settings(cors_origins="https://example.com,http://localhost:3000,https://app.example.com")
        assert settings.cors_origins == [
            "https://example.com",
            "http://localhost:3000",
            "https://app.example.com"
        ]

    def test_cors_origins_with_whitespace(self):
        """Test CORS origins with whitespace handling"""
        settings = Settings(cors_origins="https://example.com , http://localhost:3000, https://app.example.com")
        assert settings.cors_origins == [
            "https://example.com",
            "http://localhost:3000",
            "https://app.example.com"
        ]

    def test_cors_origins_empty_string(self):
        """Test CORS origins with empty string"""
        settings = Settings(cors_origins="")
        assert settings.cors_origins == ["http://localhost:3000"]

    def test_cors_origins_list_format(self):
        """Test CORS origins with list format"""
        settings = Settings(cors_origins=["https://example.com", "http://localhost:3000"])
        assert settings.cors_origins == ["https://example.com", "http://localhost:3000"]

    def test_port_parsing(self):
        """Test port parsing from string to int"""
        settings = Settings(port="8080")
        assert settings.port == 8080
        assert settings.final_port == 8080

    def test_backend_port_fallback(self):
        """Test that backend_port is used when port is None"""
        settings = Settings(port=None)
        assert settings.port is None
        assert settings.final_port == 8000  # default backend_port

    def test_environment_validation(self):
        """Test environment validation"""
        settings = Settings(environment="production")
        assert settings.environment == "production"

        settings = Settings(environment="PRODUCTION")
        assert settings.environment == "production"

        with pytest.raises(ValueError):
            Settings(environment="invalid_environment")

    def test_log_level_validation(self):
        """Test log level validation"""
        settings = Settings(log_level="debug")
        assert settings.log_level == "DEBUG"

        with pytest.raises(ValueError):
            Settings(log_level="invalid_level")

    def test_secret_key_generation(self):
        """Test that secret key is generated if using default"""
        settings = Settings(secret_key="your-secret-key-here-change-in-production")
        # Should generate a new secure key
        assert settings.secret_key != "your-secret-key-here-change-in-production"
        assert len(settings.secret_key) > 20  # Generated keys should be reasonably long

    def test_custom_secret_key_preserved(self):
        """Test that custom secret key is preserved"""
        custom_key = "my-custom-secret-key-12345"
        settings = Settings(secret_key=custom_key)
        assert settings.secret_key == custom_key

    @patch.dict(os.environ, {
        "DATABASE_URL": "postgresql://user:pass@localhost/mydb",
        "DEBUG": "true",
        "ENVIRONMENT": "production",
        "SECRET_KEY": "test-secret-key",
        "CORS_ORIGINS": "https://frontend.com,http://localhost:3000"
    })
    def test_env_variable_loading(self):
        """Test loading from environment variables"""
        settings = Settings()
        assert settings.database_url == "postgresql://user:pass@localhost/mydb"
        assert settings.debug is True
        assert settings.environment == "production"
        assert settings.secret_key == "test-secret-key"
        assert settings.cors_origins == ["https://frontend.com", "http://localhost:3000"]

    def test_final_port_priority(self):
        """Test that port takes priority over backend_port"""
        settings = Settings(backend_port=8000, port=8080)
        assert settings.backend_port == 8000
        assert settings.port == 8080
        assert settings.final_port == 8080

    def test_optional_fields(self):
        """Test optional fields can be None"""
        settings = Settings()
        assert settings.api_key is None
        assert settings.github_token is None

        settings = Settings(api_key="test-api-key", github_token="test-github-token")
        assert settings.api_key == "test-api-key"
        assert settings.github_token == "test-github-token"