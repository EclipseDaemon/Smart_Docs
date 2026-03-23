from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.models.document import Document
from app.schemas.document import DocumentListResponse
from app.services.cache_service import (
    get_cached,
    set_cached,
    make_search_cache_key
)


async def search_documents(
    query: str,
    user_id: int,
    db: AsyncSession
) -> DocumentListResponse:

    if not query or not query.strip():
        return DocumentListResponse(documents=[], total=0)

    # Check cache first
    cache_key = make_search_cache_key(user_id, query)
    cached = await get_cached(cache_key)
    if cached:
        return DocumentListResponse(**cached)

    cleaned_query = " & ".join(query.strip().split())

    result = await db.execute(
        text("""
            SELECT
                id, title, original_filename, file_path,
                file_size, file_type, is_processed,
                created_at, updated_at, owner_id,
                ts_rank(search_vector, to_tsquery('english', :query)) as rank
            FROM documents
            WHERE
                owner_id = :user_id
                AND search_vector @@ to_tsquery('english', :query)
            ORDER BY rank DESC
        """),
        {
            "query": cleaned_query,
            "user_id": user_id
        }
    )

    rows = result.fetchall()

    documents = []
    for row in rows:
        doc = Document(
            id=row.id,
            title=row.title,
            original_filename=row.original_filename,
            file_path=row.file_path,
            file_size=row.file_size,
            file_type=row.file_type,
            is_processed=row.is_processed,
            created_at=row.created_at,
            updated_at=row.updated_at,
            owner_id=row.owner_id
        )
        documents.append(doc)

    response = DocumentListResponse(
        documents=documents,
        total=len(documents)
    )

    # Cache search results for 2 minutes
    await set_cached(cache_key, response.model_dump(), ttl_seconds=120)

    return response