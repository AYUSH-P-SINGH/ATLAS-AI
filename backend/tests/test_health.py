from unittest.mock import AsyncMock, patch
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_general_health(client: AsyncClient):
    """Verifies that the root health endpoint responds with online status."""
    response = await client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "Atlas AI API"


@pytest.mark.asyncio
async def test_db_health(client: AsyncClient):
    """Verifies database health endpoint by mocking connection check."""
    with patch("app.api.health.check_db_health", new_callable=AsyncMock) as mock_db:
        mock_db.return_value = {"status": "healthy", "latency_ms": 3.5}
        
        response = await client.get("/api/health/db")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["latency_ms"] == 3.5


@pytest.mark.asyncio
async def test_redis_health(client: AsyncClient):
    """Verifies Redis health endpoint by mocking ping response."""
    with patch("app.api.health.check_redis_health", new_callable=AsyncMock) as mock_redis:
        mock_redis.return_value = {"status": "healthy", "latency_ms": 0.8}
        
        response = await client.get("/api/health/redis")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["latency_ms"] == 0.8
