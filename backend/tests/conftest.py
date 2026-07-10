import asyncio
from typing import AsyncGenerator
import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from app.core.database import Base, get_db
from app.main import app

# In-memory SQLite for isolated test environments
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},  # Required for SQLite in async
)

TestingSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def initialize_db():
    """Initializes schema and tables in the isolated sqlite database."""
    async with test_engine.begin() as conn:
        # Create all tables defined in Base metadata (including users)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Provides a rollback-guaranteed transaction session for each test."""
    async with TestingSessionLocal() as session:
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()


@pytest.fixture(autouse=True)
async def override_dependencies(db_session: AsyncSession):
    """Overrides the database dependencies on the FastAPI app."""
    async def _get_test_db() -> AsyncGenerator[AsyncSession, None]:
        yield db_session
        
    app.dependency_overrides[get_db] = _get_test_db
    yield
    app.dependency_overrides.clear()


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Exposes an HTTPX AsyncClient bound to the FastAPI application."""
    # We use ASGITransport to call FastAPI routes directly
    transport = ASGITransport(app=app) # type: ignore
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client
