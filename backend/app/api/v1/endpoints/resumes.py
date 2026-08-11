from fastapi import APIRouter, File, UploadFile

from app.services.resume_service import save_resume

router = APIRouter(
    prefix="/api/v1/resumes",
    tags=["Resumes"],
)


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...)
):
    return await save_resume(file)