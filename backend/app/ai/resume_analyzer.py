import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


class ExperienceItem(BaseModel):
    company: str | None
    title: str | None
    start_date: str | None
    end_date: str | None
    summary: str | None


class EducationItem(BaseModel):
    degree: str | None
    institution: str | None
    graduation_year: str | None


class ResumeAnalysis(BaseModel):
    name: str | None
    email: str | None
    skills: list[str]
    experience: list[ExperienceItem]
    education: list[EducationItem]


def analyze_resume(resume_text: str) -> dict[str, object]:
    completion = client.chat.completions.parse(
        model="gpt-5.4-nano",
        messages=[
            {
                "role": "system",
                "content": (
                    "Extract structured candidate information from the resume. "
                    "Do not invent information that is not present in the resume. "
                    "If a value cannot be determined, return null. "
                    "Extract each professional experience as a separate item with "
                    "company, title, start date, end date, and a concise summary. "
                    "Extract each education entry separately with degree, institution, "
                    "and graduation year."
                ),
            },
            {
                "role": "user",
                "content": resume_text,
            },
        ],
        response_format=ResumeAnalysis,
    )

    analysis = completion.choices[0].message.parsed

    if analysis is None:
        raise ValueError("OpenAI did not return a valid resume analysis.")

    return analysis.model_dump()