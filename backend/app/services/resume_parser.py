import re
from pathlib import Path

from docx import Document
from pypdf import PdfReader


def extract_text(file_path: Path) -> str:
    extension = file_path.suffix.lower()

    if extension == ".pdf":
        reader = PdfReader(file_path)
        return "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )

    if extension == ".docx":
        document = Document(file_path)
        return "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )

    raise ValueError("Unsupported resume format.")
def clean_text(text: str) -> str:
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()