"""Tests for prompt edit API endpoints"""

import json

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_prompt_edit.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_db():
    """Clean database before each test"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


def test_submit_prompt_basic():
    """Test basic prompt submission"""
    response = client.post(
        "/api/prompt/submit",
        json={
            "prompt": "Add a hello world function",
            "dry_run": True,
            "llm_provider": "mock",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert data["status"] == "plan_generated"
    assert len(data["edit_plans"]) > 0


def test_submit_prompt_with_context():
    """Test prompt submission with repository context"""
    response = client.post(
        "/api/prompt/submit",
        json={
            "prompt": "Add error handling to the authentication function",
            "repo_context": {
                "repo_path": "/test/repo",
                "language": "python",
                "framework": "FastAPI",
                "files": ["app/auth.py"],
            },
            "target_files": ["app/auth.py"],
            "dry_run": True,
            "llm_provider": "mock",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert data["status"] == "plan_generated"


def test_preview_diffs():
    """Test diff preview endpoint"""
    # First submit a prompt
    submit_response = client.post(
        "/api/prompt/submit",
        json={
            "prompt": "Add a test function",
            "target_files": ["test.py"],
            "dry_run": True,
            "llm_provider": "mock",
        },
    )
    session_id = submit_response.json()["session_id"]

    # Preview diffs
    response = client.get(f"/api/prompt/{session_id}/preview")

    assert response.status_code == 200
    data = response.json()
    assert "diffs" in data
    assert "total_files" in data
    assert data["session_id"] == session_id


def test_preview_diffs_not_found():
    """Test preview with non-existent session"""
    response = client.get("/api/prompt/invalid-session-id/preview")
    assert response.status_code == 404


def test_validate_edits():
    """Test edit validation"""
    # Submit prompt
    submit_response = client.post(
        "/api/prompt/submit",
        json={
            "prompt": "Create a Python file",
            "target_files": ["example.py"],
            "dry_run": True,
            "llm_provider": "mock",
        },
    )
    session_id = submit_response.json()["session_id"]

    # Validate
    response = client.post(
        f"/api/prompt/{session_id}/validate",
        json={"validation_types": ["syntax"]},
    )

    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert "overall_status" in data
    assert data["session_id"] == session_id


def test_format_files():
    """Test file formatting"""
    # Submit prompt
    submit_response = client.post(
        "/api/prompt/submit",
        json={
            "prompt": "Create a Python module",
            "target_files": ["module.py"],
            "dry_run": True,
            "llm_provider": "mock",
        },
    )
    session_id = submit_response.json()["session_id"]

    # Format
    response = client.post(
        f"/api/prompt/{session_id}/format",
        json={"formatters": ["black"]},
    )

    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert "total_formatted" in data


def test_get_session_status():
    """Test getting session status"""
    # Submit prompt
    submit_response = client.post(
        "/api/prompt/submit",
        json={
            "prompt": "Test prompt",
            "dry_run": True,
            "llm_provider": "mock",
        },
    )
    session_id = submit_response.json()["session_id"]

    # Get status
    response = client.get(f"/api/prompt/{session_id}/status")

    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == session_id
    assert "status" in data
    assert "prompt" in data
    assert "edit_count" in data
    assert data["prompt"] == "Test prompt"


def test_session_status_not_found():
    """Test status for non-existent session"""
    response = client.get("/api/prompt/invalid-session/status")
    assert response.status_code == 404


def test_multiple_target_files():
    """Test with multiple target files"""
    response = client.post(
        "/api/prompt/submit",
        json={
            "prompt": "Add logging to all modules",
            "target_files": ["module1.py", "module2.py", "module3.py"],
            "dry_run": True,
            "llm_provider": "mock",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data["edit_plans"]) <= 3


def test_workflow_sequence():
    """Test complete workflow: submit -> preview -> validate -> format"""
    # 1. Submit
    submit_response = client.post(
        "/api/prompt/submit",
        json={
            "prompt": "Create a utility function",
            "target_files": ["utils.py"],
            "dry_run": True,
            "llm_provider": "mock",
        },
    )
    assert submit_response.status_code == 200
    session_id = submit_response.json()["session_id"]

    # 2. Preview
    preview_response = client.get(f"/api/prompt/{session_id}/preview")
    assert preview_response.status_code == 200

    # 3. Validate
    validate_response = client.post(
        f"/api/prompt/{session_id}/validate",
        json={"validation_types": ["syntax"]},
    )
    assert validate_response.status_code == 200

    # 4. Format
    format_response = client.post(
        f"/api/prompt/{session_id}/format",
        json={},
    )
    assert format_response.status_code == 200

    # 5. Check status
    status_response = client.get(f"/api/prompt/{session_id}/status")
    assert status_response.status_code == 200
    status = status_response.json()
    assert status["validated"] is True
    assert status["formatted"] is True


def test_llm_provider_validation():
    """Test different LLM providers"""
    providers = ["mock", "openai", "anthropic"]

    for provider in providers:
        response = client.post(
            "/api/prompt/submit",
            json={
                "prompt": f"Test with {provider}",
                "dry_run": True,
                "llm_provider": provider,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "session_id" in data


def test_empty_prompt():
    """Test handling of empty prompt"""
    response = client.post(
        "/api/prompt/submit",
        json={
            "prompt": "",
            "dry_run": True,
            "llm_provider": "mock",
        },
    )
    # Should still work, just generate minimal plan
    assert response.status_code in [200, 422]


def test_validate_with_invalid_session():
    """Test validation with invalid session"""
    response = client.post(
        "/api/prompt/invalid/validate",
        json={"validation_types": ["syntax"]},
    )
    assert response.status_code == 404


def test_format_with_invalid_session():
    """Test formatting with invalid session"""
    response = client.post(
        "/api/prompt/invalid/format",
        json={},
    )
    assert response.status_code == 404
