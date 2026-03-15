import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Arrange-Act-Assert (AAA) pattern is used in all tests

def test_get_activities():
    # Arrange: (nothing to arrange for a GET)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister_participant():
    # Arrange
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Ensure clean state
    client.delete(f"/activities/{activity}/unregister?email={email}")
    # Act: Sign up
    signup_resp = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert signup_resp.status_code == 200
    assert f"Signed up {email}" in signup_resp.json()["message"]
    # Act: Unregister
    unregister_resp = client.delete(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert unregister_resp.status_code == 200
    assert f"Removed {email}" in unregister_resp.json()["message"]

def test_signup_duplicate_participant():
    # Arrange
    activity = "Chess Club"
    email = "duplicate@mergington.edu"
    client.delete(f"/activities/{activity}/unregister?email={email}")
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert resp.status_code == 400
    assert "already signed up" in resp.json()["detail"]
    # Cleanup
    client.delete(f"/activities/{activity}/unregister?email={email}")

def test_unregister_nonexistent_participant():
    # Arrange
    activity = "Chess Club"
    email = "notfound@mergington.edu"
    client.delete(f"/activities/{activity}/unregister?email={email}")
    # Act
    resp = client.delete(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert resp.status_code == 404
    assert "Participant not found" in resp.json()["detail"]
