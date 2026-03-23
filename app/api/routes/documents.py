from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.api.dependencies import get_current_active_user
from app.models.user import User
from app.schemas.document import DocumentResponse, DocumentListResponse, DocumentDetailResponse
from app.services.document_service import (
    upload_document,
    get_user_documents,
    get_document_by_id,
    delete_document
)

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload", response_model=DocumentResponse, status_code=201)
async def upload_document_endpoint(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return await upload_document(file, current_user.id, db, background_tasks)


@router.get("", response_model=DocumentListResponse)
async def list_documents(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return await get_user_documents(current_user.id, db)


@router.get("/{document_id}", response_model=DocumentDetailResponse)
async def get_document(
    document_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return await get_document_by_id(document_id, current_user.id, db)


@router.delete("/{document_id}", status_code=204)
async def delete_document_endpoint(
    document_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    await delete_document(document_id, current_user.id, db)