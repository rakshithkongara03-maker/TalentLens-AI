from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile

router = APIRouter(
    prefix="/api/v1/resumes",
    tags=["Resumes"],
)

UPLOAD_DIRECTORY = Path("uploads/resumes")
UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)
ALLOWED_EXTENSIONS = {".pdf", ".docx"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...)
):
    file_extension = Path(file.filename).suffix.lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
        status_code=400,
        detail="Only PDF and DOCX resume files are allowed.",
    )
    unique_filename = f"{uuid4()}{file_extension}"
    destination = UPLOAD_DIRECTORY / unique_filename

    file_content = await file.read()
    if len(file_content) > MAX_FILE_SIZE:
      raise HTTPException(
        status_code=400,
        detail="Resume file size must be 5 MB or less.",
    )

    with destination.open("wb") as saved_file:
        saved_file.write(file_content)

    return {
        "original_filename": file.filename,
        "stored_filename": unique_filename,
        "content_type": file.content_type,
        "size_bytes": len(file_content),
        "status": "uploaded",
    }