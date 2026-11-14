
from pydantic import BaseModel, Field, field_validator

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
    Depends
)

from pathlib import Path
from uuid import uuid4

from app.services.pdf_service import extract_text
from app.services.rag_service import answer_question
from app.services.chunking_service import create_chunks
from app.services.vector_store import store_chunks, delete_document_chunks

from app.services.auth_dependency import get_current_user
from app.services.document_service import (
    save_document,
    verify_document_owner
)


class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)

    @field_validator("question")
    @classmethod
    def validate_question(cls, value):
        if not value.strip():
            raise ValueError("Question cannot contain only spaces")

        return value.strip()


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):

    # Step 1: Validate file extension
    if not file.filename or Path(file.filename).suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    unique_filename = f"{uuid4()}_{file.filename}"
    file_path = UPLOAD_DIR / unique_filename

    # Step 2: Read and validate file size
    contents = await file.read()

    MAX_FILE_SIZE = 10 * 1024 * 1024

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size must not exceed 10 MB"
        )

    # Step 3: Validate PDF signature
    if not contents.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=400,
            detail="Invalid PDF file"
        )

    # Step 4: Save PDF
    with open(file_path, "wb") as f:
        f.write(contents)

    # Step 5: Extract text and create chunks
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

    document_id = str(uuid4())

    # Step 6: Store chunks and document ownership
    try:
        store_chunks(chunks, document_id)

        save_document(
            document_id=document_id,
            user_id=current_user["id"],
            filename=file.filename
        )

    except Exception as e:

        try:
            delete_document_chunks(document_id)
        except Exception as cleanup_error:
            print("Cleanup failed:", cleanup_error)

        file_path.unlink(missing_ok=True)

        raise HTTPException(
            status_code=500,
            detail="Failed to store PDF data. Please try again."
        ) from e

    # Step 7: Calculate extracted characters
    total_characters = sum(
        len(page["text"]) for page in extracted_text
    )

    # Step 8: Return upload response
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


@router.post("/{document_id}/ask")
async def ask_question(
    document_id: str,
    request: QuestionRequest,
    current_user: dict = Depends(get_current_user)
):

    # Step 1: Verify document ownership
    is_owner = verify_document_owner(
        document_id=document_id,
        user_id=current_user["id"]
    )

    if not is_owner:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    # Step 2: Generate answer using RAG
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
