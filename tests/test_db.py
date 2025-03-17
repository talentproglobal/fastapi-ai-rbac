import unittest
from app.db import get_user, create_user, users_collection

class TestDatabase(unittest.TestCase):
    
    def test_create_user(self):
        """
        Test if a new user can be successfully created in the database.
        """
        test_user = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "test123"
        }
        create_user(test_user)
        user = get_user("testuser")
        self.assertIsNotNone(user)
        self.assertEqual(user["username"], "testuser")

    def test_get_nonexistent_user(self):
        """
        Test if trying to fetch a non-existent user returns None.
        """
        user = get_user("nonexistent")
        self.assertIsNone(user)

if __name__ == "__main__":
    unittest.main()