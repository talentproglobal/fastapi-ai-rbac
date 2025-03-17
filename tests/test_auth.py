import unittest
from app.auth import hash_password, verify_password, create_access_token
from datetime import timedelta
import jwt
import os

SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key_here")
ALGORITHM = "HS256"

class TestAuth(unittest.TestCase):
    
    def test_password_hashing(self):
        """
        Test if a password is properly hashed and can be verified correctly.
        """
        password = "test123"
        hashed = hash_password(password)
        self.assertTrue(verify_password(password, hashed))

    def test_token_generation(self):
        """
        Test if a JWT token is correctly generated and contains the right payload.
        """
        data = {"sub": "testuser"}
        token = create_access_token(data, timedelta(minutes=30))
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        self.assertEqual(decoded["sub"], "testuser")

if __name__ == "__main__":
    unittest.main()