import os
import uuid
from pathlib import Path
from fastapi import UploadFile
from app.config import settings


ALLOWED_TYPES = {
    "application/pdf": "pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
    "application/msword": "doc"
}


def get_file_extension(content_type: str) -> str:
    return ALLOWED_TYPES.get(content_type, "")


def is_allowed_file(content_type: str) -> bool:
    return content_type in ALLOWED_TYPES


async def save_upload_file(file: UploadFile, user_id: int) -> tuple[str, int]:
    user_upload_dir = Path(settings.UPLOAD_DIR) / str(user_id)
    user_upload_dir.mkdir(parents=True, exist_ok=True)

    extension = get_file_extension(file.content_type)
    unique_filename = f"{uuid.uuid4()}.{extension}"
    file_path = user_upload_dir / unique_filename

    content = await file.read()
    file_size = len(content)

    with open(file_path, "wb") as f:
        f.write(content)

    return str(file_path).replace("\\", "/"), file_size


def extract_text_from_file(file_path: str, file_type: str) -> str:
    try:
        if file_type == "pdf":
            return _extract_from_pdf(file_path)
        elif file_type in ("docx", "doc"):
            return _extract_from_docx(file_path)
        return ""
    except Exception as e:
        print(f"EXTRACTION ERROR: {e}")
        return ""


def _extract_from_pdf(file_path: str) -> str:
    from PyPDF2 import PdfReader
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text.strip()


def _extract_from_docx(file_path: str) -> str:
    from docx import Document
    doc = Document(file_path)
    text = "\n".join(
        paragraph.text
        for paragraph in doc.paragraphs
        if paragraph.text.strip()
    )
    return text.strip()