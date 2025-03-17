from fastapi import FastAPI, HTTPException, Depends, status, UploadFile, File, Query
from fastapi.security import OAuth2PasswordRequestForm
from app.db import create_user, get_user, users_collection, save_pdf_text, get_pdf_content  # ✅ Includes PDF functions
from app.auth import authenticate_user, create_access_token, get_current_user, hash_password
from app.permissions import check_permission
from app.models import UserCreate
from datetime import timedelta
import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer, util

app = FastAPI(title="FastAPI AI-RBAC", description="JWT Authentication with MongoDB & AI")

# ✅ Load AI model for answering questions
model = SentenceTransformer("all-MiniLM-L6-v2")

# ✅ User Registration (Open to All)
@app.post("/register/")
def register(user: UserCreate):
    existing_user = get_user(user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = {
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "hashed_password": hash_password(user.password),  # ✅ Correct password hashing
        "role": "user"
    }
    
    users_collection.insert_one(new_user)  # ✅ Use MongoDB insert
    return {"message": "User registered successfully"}

# ✅ Login (Generate JWT Token)
@app.post("/token/", response_model=dict)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": user["username"]}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}

# ✅ Get Current User (Requires Authentication)
@app.get("/users/me/", response_model=dict)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    return {"username": current_user["username"], "role": current_user["role"]}

# ✅ Admin-Only Endpoint (Protected by RBAC)
@app.get("/admin/", dependencies=[Depends(lambda: check_permission("delete"))])
async def admin_dashboard():
    return {"message": "Welcome, Admin! You have full access."}

# ✅ AI-Based Question Answering (Mock Example)
@app.get("/ask/")
async def ask_question(query: str):
    return {"question": query, "answer": "This is a placeholder answer from AI."}

# ✅ Protected AI Feature (Only Accessible by Authenticated Users)
@app.get("/ai/protected/", dependencies=[Depends(get_current_user)])
async def protected_ai_feature():
    return {"message": "This AI feature is only for logged-in users."}

# ✅ PDF Upload API
@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    """ Upload a PDF, extract text, and store it in MongoDB """
    contents = await file.read()
    pdf_document = fitz.open(stream=contents, filetype="pdf")

    text = ""
    for page in pdf_document:
        text += page.get_text("text")

    if not text.strip():
        raise HTTPException(status_code=400, detail="PDF contains no readable text.")

    # ✅ Save extracted text in MongoDB
    save_pdf_text(file.filename, text)

    return {"message": "PDF uploaded successfully", "filename": file.filename}

# ✅ Ask Questions from PDF API
@app.get("/ask-pdf/")
async def ask_pdf(query: str = Query(..., min_length=3), filename: str = Query(...)):
    """ Answer questions based on uploaded PDF """
    content = get_pdf_content(filename)
    
    if not content:
        raise HTTPException(status_code=404, detail="PDF not found")

    sentences = content.split("\n")

    # ✅ Find most relevant sentence
    query_embedding = model.encode(query, convert_to_tensor=True)
    sentence_embeddings = model.encode(sentences, convert_to_tensor=True)

    scores = util.pytorch_cos_sim(query_embedding, sentence_embeddings)[0]
    best_match_index = scores.argmax()

    return {
        "query": query,
        "answer": sentences[best_match_index] if best_match_index >= 0 else "No relevant answer found"
    }