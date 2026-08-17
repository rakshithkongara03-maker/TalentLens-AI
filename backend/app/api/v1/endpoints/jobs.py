from fastapi import APIRouter

from app.ai.job_analyzer import analyze_job
from app.schemas.job import JobDescriptionRequest


router = APIRouter(
    prefix="/api/v1/jobs",
    tags=["Jobs"],
)


@router.post("/analyze")
async def analyze_job_description(request: JobDescriptionRequest):
    analysis = analyze_job(request.job_description)

    return {
        "status": "analyzed",
        "analysis": analysis,
    }