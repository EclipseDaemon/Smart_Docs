import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool

from app.main import app
from app.db.base import Base
from app.db.session import get_db
from app.config import settings

# Use a separate test database
TEST_DATABASE_URL = settings.DATABASE_URL.replace(
    "/smartdocs_db",
    "/smartdocs_test_db"
)

# Test engine with NullPool — no connection reuse between tests
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    poolclass=NullPool
)

TestSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)


async def override_get_db():
    async with TestSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_test_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()


@pytest_asyncio.fixture(autouse=True)
async def clean_tables():
    yield
    async with test_engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(table.delete())


@pytest_asyncio.fixture
async def client():
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def registered_user(client: AsyncClient):
    response = await client.post("/auth/register", json={
        "email": "test@smartdocs.com",
        "password": "testpassword123",
        "full_name": "Test User"
    })
    return response.json()


@pytest_asyncio.fixture
async def auth_headers(client: AsyncClient):
    await client.post("/auth/register", json={
        "email": "test@smartdocs.com",
        "password": "testpassword123",
        "full_name": "Test User"
    })
    response = await client.post(
        "/auth/login",
        data={
            "username": "test@smartdocs.com",
            "password": "testpassword123"
        }
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}