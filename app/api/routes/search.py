from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.api.dependencies import get_current_active_user
from app.models.user import User
from app.schemas.document import DocumentListResponse
from app.services.search_service import search_documents

router = APIRouter(prefix="/search", tags=["Search"])


@router.get("", response_model=DocumentListResponse)
async def search(
    q: str = Query(..., min_length=1, description="Search query"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return await search_documents(q, current_user.id, db)