import time
from typing import Optional
from redis.asyncio import ConnectionPool, Redis
from loguru import logger
from app.core.config import settings

# Global connection pool and client references
_redis_pool: Optional[ConnectionPool] = None
redis_client: Optional[Redis] = None


async def init_redis() -> Optional[Redis]:
    """Initializes the Redis connection pool and async client."""
    global _redis_pool, redis_client
    try:
        logger.info(f"Initializing Redis pool connection to {settings.REDIS_URL}...")
        _redis_pool = ConnectionPool.from_url(
            settings.REDIS_URL,
            decode_responses=True,
            max_connections=50,  # Limits maximum pool connections
        )
        redis_client = Redis(connection_pool=_redis_pool)
        
        # Verify connection on startup
        # We use a short timeout so boot isn't blocked too long if Redis is down
        await redis_client.ping()
        logger.info("Redis connection established successfully.")
        return redis_client
    except Exception as e:
        logger.warning(
            f"Failed to connect to Redis on startup. Application will run, but cache operations will be disabled. Error: {e}"
        )
        # We keep the client reference but operations will fail or fallback
        return None


async def close_redis() -> None:
    """Closes the Redis connection pool gracefully on shutdown."""
    global _redis_pool, redis_client
    if redis_client:
        logger.info("Closing Redis client...")
        await redis_client.close()
    if _redis_pool:
        logger.info("Disconnecting Redis connection pool...")
        await _redis_pool.disconnect()
    logger.info("Redis client and pool shut down.")


async def check_redis_health() -> dict:
    """Performs a PING command to verify Redis responsiveness and reports latency."""
    if redis_client is None:
        return {"status": "unhealthy", "error": "Redis client not initialized"}
    
    start_time = time.time()
    try:
        # Check connection responsiveness
        await redis_client.ping()
        latency = (time.time() - start_time) * 1000  # ms
        return {"status": "healthy", "latency_ms": round(latency, 2)}
    except Exception as e:
        latency = (time.time() - start_time) * 1000
        logger.error(f"Redis health check failed: {e}")
        return {"status": "unhealthy", "error": str(e), "latency_ms": round(latency, 2)}
