from fastapi import APIRouter
from app.core.database import check_db_health
from app.core.redis import check_redis_health

router = APIRouter(prefix="/health", tags=["Health Checks"])


@router.get("")
async def general_health():
    """General health check of the FastAPI API gateway."""
    return {"status": "healthy", "service": "Atlas AI API"}


@router.get("/db")
async def db_health():
    """Evaluates connection state and latency to the PostgreSQL database."""
    health = await check_db_health()
    return health


@router.get("/redis")
async def redis_health():
    """Evaluates connection state and latency to the Redis cache cluster."""
    health = await check_redis_health()
    return health
