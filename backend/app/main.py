from fastapi import FastAPI
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.resumes import router as resumes_router

app = FastAPI(
    title="TalentLens-AI API",
    description="AI-powered resume analysis and candidate matching platform.",
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(resumes_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to TalentLens-AI",
        "status": "running",
    }