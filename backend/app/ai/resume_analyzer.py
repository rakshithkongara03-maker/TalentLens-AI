import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


class ResumeAnalysis(BaseModel):
    name: str | None
    email: str | None
    skills: list[str]
    experience: list[str]
    education: list[str]


def analyze_resume(resume_text: str) -> dict[str, object]:
    completion = client.chat.completions.parse(
        model="gpt-5.4-nano",
        messages=[
            {
                "role": "system",
                "content": (
                    "Extract structured candidate information from the resume. "
                    "Do not invent information. If a name or email is missing, return null. "
                    "Return skills, experience, and education only when supported by the resume."
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