from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DocumentResponse(BaseModel):
    id: int
    title: str
    original_filename: str
    file_size: int
    file_type: str
    is_processed: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class DocumentListResponse(BaseModel):
    documents: list[DocumentResponse]
    total: int


class DocumentDetailResponse(DocumentResponse):
    content: Optional[str] = None