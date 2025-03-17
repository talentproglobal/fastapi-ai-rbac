import unittest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestPDF(unittest.TestCase):
    
    def test_pdf_upload(self):
        """
        Test if a PDF file can be uploaded successfully.
        """
        files = {"file": ("test.pdf", b"Fake PDF Content", "application/pdf")}
        response = client.post("/upload-pdf/", files=files)
        self.assertEqual(response.status_code, 200)

    def test_ask_pdf(self):
        """
        Test if the API correctly answers questions based on an uploaded PDF.
        """
        response = client.get("/ask-pdf/", params={"query": "What is in the PDF?"})
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()