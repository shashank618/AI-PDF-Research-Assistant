

from pydantic import BaseModel, Field, field_validator

from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
from uuid import uuid4

from app.services.pdf_service import extract_text
from app.services.rag_service import answer_question
from app.services.chunking_service import create_chunks
from app.services.vector_store import store_chunks, delete_document_chunks


# ==========================================
# 1. Question Request Validation
# ==========================================

class QuestionRequest(BaseModel):

    question: str = Field(
        ...,
        min_length=1,
        max_length=500
    )

    @field_validator("question")
    @classmethod
    def validate_question(cls, value):

        if not value.strip():
            raise ValueError(
                "Question cannot contain only spaces"
            )

        return value.strip()


# ==========================================
# 2. Router Configuration
# ==========================================

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


# ==========================================
# 3. PDF Upload Endpoint
# ==========================================

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    # Step 1: Validate file extension
    if not file.filename or Path(file.filename).suffix.lower() != ".pdf":

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    # Step 2: Generate unique filename
    unique_filename = f"{uuid4()}_{file.filename}"

    file_path = UPLOAD_DIR / unique_filename

    # Step 3: Read file contents
    contents = await file.read()

    MAX_FILE_SIZE = 10 * 1024 * 1024

    if len(contents) > MAX_FILE_SIZE:

        raise HTTPException(
            status_code=413,
            detail="File size must not exceed 10 MB"
        )

    # Step 4: Validate PDF signature
    if not contents.startswith(b"%PDF-"):

        raise HTTPException(
            status_code=400,
            detail="Invalid PDF file"
        )

    # Step 5: Save PDF
    with open(file_path, "wb") as f:
        f.write(contents)

    # Step 6: Extract text and create chunks
    try:

        extracted_text = extract_text(file_path)

        chunks = create_chunks(extracted_text)

        if not chunks:

            raise HTTPException(
                status_code=400,
                detail="No readable text found in the PDF"
            )

    except HTTPException:

        file_path.unlink(missing_ok=True)
        raise

    except Exception:

        file_path.unlink(missing_ok=True)

        raise HTTPException(
            status_code=400,
            detail="Unable to read or process this PDF file"
        )

    # Step 7: Generate document ID
    document_id = str(uuid4())

    # Step 8: Store chunks in ChromaDB
    try:

        store_chunks(chunks, document_id)

    except Exception as e:

        # Remove any partially stored chunks
        try:
            delete_document_chunks(document_id)

        except Exception as cleanup_error:
            print("Cleanup failed:", cleanup_error)

        # Delete the uploaded PDF
        file_path.unlink(missing_ok=True)

        raise HTTPException(
            status_code=500,
            detail="Failed to store PDF data. Please try again."
        ) from e

    # Step 9: Calculate total characters
    total_characters = sum(
        len(page["text"]) for page in extracted_text
    )

    # Step 10: Return upload details
    return {
        "message": "PDF uploaded, processed and stored successfully",
        "filename": file.filename,
        "saved_as": unique_filename,
        "document_id": document_id,
        "total_pages": len(extracted_text),
        "total_chunks": len(chunks),
        "extracted_characters": total_characters,
        "text_preview": extracted_text[0]["text"][:500]
    }


# ==========================================
# 4. Ask Question Endpoint
# ==========================================

@router.post("/{document_id}/ask")
async def ask_question(
    document_id: str,
    request: QuestionRequest
):

    try:

        result = answer_question(
            question=request.question,
            document_id=document_id
        )

        return result

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
