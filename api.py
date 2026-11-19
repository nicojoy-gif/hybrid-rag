
from pathlib import Path
import shutil
from fastapi.responses import FileResponse
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from main import run_rag_pipeline, refresh_knowledge_base

app = FastAPI()

UPLOAD_DIR = Path("data/raw")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": "RAG API is running"}

@app.post("/ask")
def ask_question(request: QuestionRequest):
    result = run_rag_pipeline(request.question)

    return {
        "question": request.question,
        "answer": result["answer"],
        "sources": result["sources"]
    }

@app.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No filename provided."
        )

    file_extension = Path(file.filename).suffix.lower()

    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, DOCX and TXT files are allowed."
        )

    file_path = UPLOAD_DIR / Path(file.filename).name

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        refresh_knowledge_base()

    except Exception as error:
        file_path.unlink(missing_ok=True)

        raise HTTPException(
            status_code=500,
            detail=f"Document upload or indexing failed: {error}"
        )

    finally:
        await file.close()

    return {
        "message": "Document uploaded and indexed successfully",
        "filename": file_path.name
    }

@app.get("/documents")
def get_documents():
    documents = []

    for file_path in UPLOAD_DIR.iterdir():

        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in ALLOWED_EXTENSIONS:
            continue

        size_kb = round(file_path.stat().st_size / 1024, 2)

        documents.append({
            "name": file_path.name,
            "type": file_path.suffix[1:].upper(),
            "size": f"{size_kb} KB"
        })

    return {
        "documents": documents,
        "total": len(documents)
    }


@app.get("/documents/{filename}/view")
def view_document(filename: str):

    file_name = Path(filename)

    if file_name.name != filename:
        raise HTTPException(
            status_code=400,
            detail="Invalid filename."
        )

    if file_name.suffix.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported document type."
        )

    file_path = UPLOAD_DIR / filename

    if not file_path.is_file():
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    media_types = {
        ".pdf": "application/pdf",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".txt": "text/plain"
    }

    return FileResponse(
        path=file_path,
        media_type=media_types[file_path.suffix.lower()],
        filename=filename,
        content_disposition_type="inline"
    )
