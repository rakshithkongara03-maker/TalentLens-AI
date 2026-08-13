from pathlib import Path
from uuid import uuid4
from app.ai.resume_analyzer import analyze_resume
from fastapi import HTTPException, UploadFile
from app.services.resume_parser import clean_text, extract_text

UPLOAD_DIRECTORY = Path("uploads/resumes")
UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


async def save_resume(file: UploadFile) -> dict[str, object]:
    file_extension = Path(file.filename or "").suffix.lower()

    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX resume files are allowed.",
        )

    file_content = await file.read()

    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="Resume file size must be 5 MB or less.",
        )

    unique_filename = f"{uuid4()}{file_extension}"
    destination = UPLOAD_DIRECTORY / unique_filename

    with destination.open("wb") as saved_file:
        saved_file.write(file_content)
        extracted_text = extract_text(destination)
        extracted_text = clean_text(extracted_text)
        analysis = analyze_resume(extracted_text)

    return {
        "original_filename": file.filename,
        "stored_filename": unique_filename,
        "content_type": file.content_type,
        "size_bytes": len(file_content),
        "status": "uploaded",
        "extracted_text": extracted_text,
        "analysis": analysis,
    }