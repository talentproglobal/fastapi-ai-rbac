from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import create_access_token, get_current_user, get_password_hash
from app.db import get_user, create_user
from app.ai import upload_file, query_ai
from app.models import UserCreate
import os

app = FastAPI()

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form_data.username)
    if not user or not user.get("hashed_password"):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token({"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/")
def create_new_user(user: UserCreate):
    if get_user(user.username):
        raise HTTPException(status_code=400, detail="User already exists")
    new_user = create_user(user)
    return new_user

@app.get("/users/{username}")
def read_user(username: str, current_user: str = Depends(get_current_user)):
    user = get_user(username)
    return user

@app.post("/upload/")
def upload_doc(file: UploadFile = File(...)):
    return {"filename": upload_file(file)}

@app.get("/query/")
def query_doc(query: str):
    return query_ai(query)
