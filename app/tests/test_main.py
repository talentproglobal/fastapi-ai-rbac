import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db import fake_users_db, get_user, create_user
from app.auth import get_password_hash, create_access_token

client = TestClient(app)

# Sample user for testing
TEST_USER = {
    "username": "testuser",
    "full_name": "Test User",
    "email": "test@example.com",
    "password": "testpassword",
}

# Test user registration
def test_create_user():
    response = client.post("/users/", json=TEST_USER)
    assert response.status_code == 200
    assert response.json()["username"] == TEST_USER["username"]

# Test user login
def test_login():
    create_user(TEST_USER)  # Ensure user exists
    response = client.post("/token", data={"username": TEST_USER["username"], "password": TEST_USER["password"]})
    assert response.status_code == 200
    assert "access_token" in response.json()

# Test getting user details
def test_get_user():
    access_token = create_access_token({"sub": TEST_USER["username"]})
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get(f"/users/{TEST_USER['username']}", headers=headers)
    assert response.status_code == 200
    assert response.json()["username"] == TEST_USER["username"]

# Test unauthorized user access
def test_unauthorized_user():
    response = client.get(f"/users/{TEST_USER['username']}")
    assert response.status_code == 401

# Test file upload (mocked for now)
def test_upload_file():
    file_content = b"This is a test document."
    files = {"file": ("test.txt", file_content, "text/plain")}
    response = client.post("/upload/", files=files)
    assert response.status_code == 200
    assert "filename" in response.json()

# Test AI query (mocked response)
def test_query_ai():
    response = client.get("/query?query=What is AI?")
    assert response.status_code == 200
    assert "response" in response.json()

# Test admin-only user deletion (mocked admin user)
def test_delete_user():
    admin_token = create_access_token({"sub": "admin"})
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.delete(f"/users/{TEST_USER['username']}", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "User deleted"

if __name__ == "__main__":
    pytest.main()
