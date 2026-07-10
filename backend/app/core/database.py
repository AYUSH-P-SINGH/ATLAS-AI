import time
from typing import AsyncGenerator
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from loguru import logger
from app.core.config import settings

# Create async engine with connection pooling
# pool_size and max_overflow optimize concurrent request throughput
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # Automatically verify connections before using them
)

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency helper to yield async database sessions."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Database session error: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()


async def check_db_health() -> dict:
    """Verifies database connectivity and calculates query execution time."""
    start_time = time.time()
    try:
        async with AsyncSessionLocal() as session:
            # Execute simple ping query
            result = await session.execute(text("SELECT 1"))
            one = result.scalar()
            latency = (time.time() - start_time) * 1000  # ms
            if one == 1:
                return {"status": "healthy", "latency_ms": round(latency, 2)}
            return {"status": "unhealthy", "error": "Unexpected query output"}
    except Exception as e:
        latency = (time.time() - start_time) * 1000
        logger.error(f"Database health check failed: {e}")
        return {"status": "unhealthy", "error": str(e), "latency_ms": round(latency, 2)}
