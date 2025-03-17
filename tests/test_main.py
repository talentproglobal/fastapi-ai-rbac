import unittest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestMainRoutes(unittest.TestCase):
    
    def test_register(self):
        """
        Test if a user can successfully register using the API.
        """
        response = client.post("/register/", json={
            "username": "testuser",
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "test123"
        })
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        """
        Test if a user can successfully log in and receive an access token.
        """
        response = client.post("/token/", data={
            "username": "testuser",
            "password": "test123"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())

if __name__ == "__main__":
    unittest.main()