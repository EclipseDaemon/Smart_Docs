from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy import text
import structlog
import os
from app.services.cache_service import get_redis_client
from app.config import settings
from app.db.session import engine
from app.api.routes.auth import router as auth_router
from app.api.routes.documents import router as documents_router
from app.api.routes.search import router as search_router
from app.models.user import User
from app.models.document import Document

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer()
    ]
)

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("starting_application", name=settings.APP_NAME)
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    # Verify database
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
        logger.info("database_connection_verified")

    # Verify Redis
    redis = await get_redis_client()
    await redis.ping()
    logger.info("redis_connection_verified")

    logger.info("application_started_successfully")

    yield

    from app.services.cache_service import close_redis_client
    await close_redis_client()
    await engine.dispose()
    logger.info("shutting_down_application")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(documents_router)
app.include_router(search_router)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION
    }