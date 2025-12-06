"""Tests for main application"""


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_root(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "Welcome to FastAPI Backend"


def test_list_items(client):
    """Test listing items"""
    response = client.get("/api/items")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data


def test_create_item(client):
    """Test creating an item"""
    response = client.post("/api/items?name=Test&description=Test Item")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test"
    assert data["description"] == "Test Item"


def test_get_item(client):
    """Test getting item by ID"""
    response = client.get("/api/items/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
