import unittest
from app.permissions import check_permission

class TestPermissions(unittest.TestCase):

    def test_admin_permissions(self):
        """
        Test if an admin user has the correct permissions.
        """
        self.assertTrue(check_permission("admin", "delete"))
        self.assertTrue(check_permission("admin", "write"))

    def test_user_permissions(self):
        """
        Test if a normal user does NOT have admin-level permissions.
        """
        self.assertTrue(check_permission("user", "read"))
        self.assertFalse(check_permission("user", "delete"))

if __name__ == "__main__":
    unittest.main()