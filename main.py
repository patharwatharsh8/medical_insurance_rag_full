import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
from chunker import chunk_text
from embeddings import embed_text
from retriever import pc
from rag_pipeline import rag_answer
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

DATA_DIR = "../data"
os.makedirs(DATA_DIR, exist_ok=True)

@app.get("/")
def root():
    return {"msg": "Health Insurance RAG API running"}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = f"{DATA_DIR}/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    reader = PdfReader(file_path)
    pages = [page.extract_text() for page in reader.pages]
    full_text = "\n".join(pages)

    chunks = chunk_text(full_text, method="recursive")

    pinecone_index = pc.Index(os.getenv("PINECONE_INDEX"))

    for idx, chunk in enumerate(chunks):
        vector = embed_text(chunk)

        pinecone_index.upsert([
            (f"chunk_{uuid.uuid4()}", vector, {"text": chunk, "page": idx + 1})
        ])

    return {"status": "success", "chunks": len(chunks)}

@app.post("/ask")
async def ask_question(query: str = Form(...)):
    output = rag_answer(query)
    return output
