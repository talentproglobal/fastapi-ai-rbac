from pymongo import MongoClient
from bson import ObjectId

client = MongoClient("mongodb://localhost:27017")
db = client.fastapi_db

def get_user(username):
    return db.users.find_one({"username": username})

def create_user(user):
    user_data = user.dict()
    user_data["_id"] = str(ObjectId())  # Assign MongoDB ObjectId
    user_data["hashed_password"] = user_data.pop("password")  # Hash password separately
    db.users.insert_one(user_data)
    return user_data
