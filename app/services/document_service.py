from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import UploadFile, BackgroundTasks

from app.models.document import Document
from app.schemas.document import DocumentListResponse, DocumentResponse
from app.core.exceptions import (
    FileTooLargeException,
    UnsupportedFileTypeException,
    DocumentNotFoundException
)
from app.utils.file_processor import (
    save_upload_file,
    extract_text_from_file,
    is_allowed_file,
    get_file_extension
)
from app.services.cache_service import (
    get_cached,
    set_cached,
    delete_cached,
    make_documents_cache_key
)
from app.config import settings


async def upload_document(
    file: UploadFile,
    user_id: int,
    db: AsyncSession,
    background_tasks: BackgroundTasks
) -> Document:
    if not is_allowed_file(file.content_type):
        raise UnsupportedFileTypeException()

    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)

    max_size = settings.MAX_FILE_SIZE_MB * 1024 * 1024
    if file_size > max_size:
        raise FileTooLargeException(settings.MAX_FILE_SIZE_MB)

    file_path, actual_size = await save_upload_file(file, user_id)
    file_type = get_file_extension(file.content_type)

    document = Document(
        title=file.filename or "Untitled",
        original_filename=file.filename or "untitled",
        file_path=file_path,
        file_size=actual_size,
        file_type=file_type,
        is_processed=False,
        owner_id=user_id
    )

    db.add(document)
    await db.flush()
    await db.refresh(document)
    await db.commit()
    await db.refresh(document)

    document_id = document.id

    # Invalidate document list cache for this user
    await delete_cached(make_documents_cache_key(user_id))

    background_tasks.add_task(
        process_document,
        document_id,
        file_path,
        file_type
    )

    return document


async def process_document(
    document_id: int,
    file_path: str,
    file_type: str
) -> None:
    import structlog
    from sqlalchemy import text
    logger = structlog.get_logger()

    try:
        logger.info("processing_document", document_id=document_id)
        extracted_text = extract_text_from_file(file_path, file_type)
        logger.info("extraction_complete", document_id=document_id, length=len(extracted_text))

        from app.db.session import AsyncSessionLocal
        async with AsyncSessionLocal() as db:
            try:
                result = await db.execute(
                    select(Document).where(Document.id == document_id)
                )
                document = result.scalar_one_or_none()

                if document:
                    document.content = extracted_text
                    document.is_processed = True

                    await db.execute(
                        text("""
                            UPDATE documents
                            SET search_vector = (
                                setweight(to_tsvector('english', COALESCE(:title, '')), 'A') ||
                                setweight(to_tsvector('english', COALESCE(:content, '')), 'B')
                            )
                            WHERE id = :doc_id
                        """),
                        {
                            "title": document.title,
                            "content": extracted_text,
                            "doc_id": document_id
                        }
                    )

                    await db.commit()
                    logger.info("document_processed_successfully", document_id=document_id)

                    # Invalidate cache after processing
                    await delete_cached(make_documents_cache_key(document.owner_id))

                else:
                    logger.error("document_not_found", document_id=document_id)

            except Exception as e:
                await db.rollback()
                logger.error("db_update_failed", document_id=document_id, error=str(e))

    except Exception as e:
        logger.error("processing_failed", document_id=document_id, error=str(e))


async def get_user_documents(
    user_id: int,
    db: AsyncSession
) -> DocumentListResponse:
    cache_key = make_documents_cache_key(user_id)

    # Try cache first
    cached = await get_cached(cache_key)
    if cached:
        return DocumentListResponse(**cached)

    # Cache miss — query database
    result = await db.execute(
        select(Document)
        .where(Document.owner_id == user_id)
        .order_by(Document.created_at.desc())
    )
    documents = result.scalars().all()

    response = DocumentListResponse(
        documents=list(documents),
        total=len(documents)
    )

    # Store in cache
    await set_cached(
        cache_key,
        response.model_dump(),
        ttl_seconds=300
    )

    return response


async def get_document_by_id(
    document_id: int,
    user_id: int,
    db: AsyncSession
) -> Document:
    result = await db.execute(
        select(Document).where(
            Document.id == document_id,
            Document.owner_id == user_id
        )
    )
    document = result.scalar_one_or_none()
    if not document:
        raise DocumentNotFoundException()
    return document


async def delete_document(
    document_id: int,
    user_id: int,
    db: AsyncSession
) -> None:
    document = await get_document_by_id(document_id, user_id, db)

    import os
    if os.path.exists(document.file_path):
        os.remove(document.file_path)

    await db.delete(document)

    # Invalidate cache
    await delete_cached(make_documents_cache_key(user_id))