import unittest
from app.ai import process_query

class TestAI(unittest.TestCase):

    def test_ai_response(self):
        """
        Test if the AI processing function returns a valid response.
        """
        response = process_query("What is AI?")
        self.assertIsInstance(response, str)

if __name__ == "__main__":
    unittest.main()