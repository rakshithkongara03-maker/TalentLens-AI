from pydantic import BaseModel


class JobDescriptionRequest(BaseModel):
    job_description: str