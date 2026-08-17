import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


class JobAnalysis(BaseModel):
    job_title: str | None
    required_skills: list[str]
    preferred_skills: list[str]
    experience_required: str | None
    education_required: str | None
    responsibilities: list[str]


def analyze_job(job_description: str) -> dict[str, object]:
    completion = client.chat.completions.parse(
        model="gpt-5.4-nano",
        messages=[
            {
                "role": "system",
                "content": (
                    "Extract structured information from the job description. "
                    "Do not invent requirements that are not present. "
                    "If a value cannot be determined, return null. "
                    "Separate required skills from preferred skills when possible."
                ),
            },
            {
                "role": "user",
                "content": job_description,
            },
        ],
        response_format=JobAnalysis,
    )

    analysis = completion.choices[0].message.parsed

    if analysis is None:
        raise ValueError("OpenAI did not return a valid job analysis.")

    return analysis.model_dump()