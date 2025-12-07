"""Tests for configuration management"""

import os
from unittest import mock

import pytest

from app.config import Settings


def test_default_settings():
    """Test default settings without environment variables"""
    with mock.patch.dict(os.environ, {}, clear=True):
        settings = Settings()
        assert settings.environment == "development"
        assert settings.backend_host == "0.0.0.0"
        assert settings.app_name == "FastAPI Backend"


def test_port_preference():
    """Test that PORT env var is preferred over BACKEND_PORT"""
    with mock.patch.dict(os.environ, {"PORT": "9000", "BACKEND_PORT": "8000"}, clear=True):
        settings = Settings()
        assert settings.backend_port == 9000

    with mock.patch.dict(os.environ, {"BACKEND_PORT": "8000"}, clear=True):
        settings = Settings()
        assert settings.backend_port == 8000


def test_cors_origins_parsing():
    """Test CORS origins parsing from comma-separated string"""
    with mock.patch.dict(os.environ, {"CORS_ORIGINS": "http://localhost:3000,https://example.com"}, clear=True):
        settings = Settings()
        assert settings.cors_origins == ["http://localhost:3000", "https://example.com"]

    with mock.patch.dict(os.environ, {"CORS_ORIGINS": "http://localhost:3000, https://example.com"}, clear=True):
        settings = Settings()
        assert settings.cors_origins == ["http://localhost:3000", "https://example.com"]


def test_environment_based_defaults():
    """Test that debug and log_level are set based on environment"""
    with mock.patch.dict(os.environ, {"ENVIRONMENT": "development"}, clear=True):
        settings = Settings()
        assert settings.environment == "development"
        assert settings.debug is True
        assert settings.log_level == "DEBUG"

    with mock.patch.dict(os.environ, {"ENVIRONMENT": "production"}, clear=True):
        settings = Settings()
        assert settings.environment == "production"
        assert settings.debug is False
        assert settings.log_level == "INFO"


def test_environment_normalization():
    """Test that environment is normalized to lowercase"""
    with mock.patch.dict(os.environ, {"ENVIRONMENT": "PRODUCTION"}, clear=True):
        settings = Settings()
        assert settings.environment == "production"


def test_is_production_method():
    """Test is_production helper method"""
    with mock.patch.dict(os.environ, {"ENVIRONMENT": "production"}, clear=True):
        settings = Settings()
        assert settings.is_production() is True
        assert settings.is_development() is False


def test_is_development_method():
    """Test is_development helper method"""
    with mock.patch.dict(os.environ, {"ENVIRONMENT": "development"}, clear=True):
        settings = Settings()
        assert settings.is_development() is True
        assert settings.is_production() is False
