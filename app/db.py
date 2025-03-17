from pymongo import MongoClient
from bson import ObjectId
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "fastapi_db")

# Initialize MongoDB Connection
try:
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    users_collection = db["users"]
    documents_collection = db["documents"]  # ✅ Collection for storing PDFs
    print("✅ Connected to MongoDB")
except Exception as e:
    print(f"❌ MongoDB Connection Failed: {e}")

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """ Hash a password before storing it in the database """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """ Verify if the provided password matches the hashed password """
    return pwd_context.verify(plain_password, hashed_password)

def get_user(username: str):
    """ Retrieve a user by username """
    user = users_collection.find_one({"username": username})
    if user:
        user["_id"] = str(user["_id"])  # Convert ObjectId to string
    return user

def create_user(user):
    """ Create a new user in MongoDB """
    user_data = dict(user)
    user_data["_id"] = str(ObjectId())  # Assign MongoDB ObjectId
    user_data["hashed_password"] = hash_password(user_data.pop("password"))  # Securely hash password
    users_collection.insert_one(user_data)
    return user_data

def create_admin_if_not_exists():
    """ Ensure an admin user exists in the database """
    admin_user = get_user("admin")
    if not admin_user:
        admin_data = {
            "username": "admin",
            "email": "admin@example.com",
            "hashed_password": hash_password("admin123"),
            "role": "admin"
        }
        users_collection.insert_one(admin_data)
        print("✅ Admin user created with default password: admin123")
    else:
        print("🔹 Admin user already exists")

# ✅ Function to store extracted PDF text
def save_pdf_text(filename, content):
    """ Store extracted text from a PDF in MongoDB """
    document = {
        "filename": filename,
        "content": content
    }
    documents_collection.insert_one(document)
    print(f"✅ PDF '{filename}' saved successfully!")

# ✅ Function to get stored PDF content
def get_pdf_content(filename):
    """ Retrieve stored PDF text from MongoDB """
    document = documents_collection.find_one({"filename": filename})
    return document["content"] if document else None

# Run on startup
create_admin_if_not_exists()