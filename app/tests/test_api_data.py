import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    """Test health check endpoint."""
    response = client.get("/health/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Kasparro" in response.json()["message"]
