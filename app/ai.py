from fastapi import APIRouter, Depends, UploadFile, File
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from transformers import pipeline
import fitz  # PyMuPDF for PDF text extraction
from auth import get_current_user

# Initialize AI Router
ai_router = APIRouter()

# Load Free AI Model for Q&A
qa_model = pipeline("question-answering", model="deepset/roberta-base-squad2")

# Initialize Vector Database (ChromaDB)
vector_db = None

def extract_text_from_pdf(file):
    """Extract text from a PDF file."""
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = "\n".join([page.get_text() for page in doc])
    return text

@ai_router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """ Upload a document and store its embeddings for AI search """
    global vector_db
    text = extract_text_from_pdf(file)
    
    # Convert text into embeddings using a free Hugging Face model
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_db = Chroma.from_texts([text], embedding=embeddings)

    return {"message": "File uploaded and processed successfully!"}

@ai_router.get("/ask/")
async def ask_question(query: str):
    """ Ask a question based on the uploaded document """
    if vector_db is None:
        return {"error": "No document uploaded yet!"}
    
    # Retrieve most relevant text
    retrieved_docs = vector_db.similarity_search(query, k=3)
    context = " ".join([doc.page_content for doc in retrieved_docs])

    # Get AI-generated answer
    answer = qa_model(question=query, context=context)

    return {"question": query, "answer": answer['answer']}

@ai_router.get("/ai/protected/", dependencies=[Depends(get_current_user)])
async def protected_ai_feature():
    """ AI feature only accessible by authenticated users """
    return {"message": "This AI feature is restricted to logged-in users."}