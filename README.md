kdir fastapi-ai-rbac && cd fastapi-ai-rbac
python3 -m venv venv
source venv/bin/activate  # On Windows, use source venv/Scripts/activate
pip install fastapi uvicorn jose passlib[bcrypt] python-multipart pydantic[dotenv] oso
If using AI processing:
pip install transformers sentence-transformers
