from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.core.config import settings
from app.core.logging import setup_logging
from app.core.redis import init_redis, close_redis
from app.middleware.request_id import RequestIdMiddleware
from app.middleware.logging import LoggingMiddleware
from app.middleware.security import SecurityHeadersMiddleware, RateLimitingMiddleware
from app.middleware.errors import register_error_handlers
from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.health import router as health_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle event handler for backend resource setup and teardown."""
    # Startup phase
    setup_logging()
    logger.info("Starting Atlas AI API Application lifecycle...")
    
    # Initialize Redis connection pool
    await init_redis()
    
    yield
    
    # Shutdown phase
    logger.info("Stopping Atlas AI API Application lifecycle...")
    await close_redis()
    logger.info("Atlas AI API lifecycle terminated.")


app = FastAPI(
    title="Atlas AI API",
    description="Software Architecture Copilot Backend Service",
    version="0.1.0",
    lifespan=lifespan,
)

# 1. Register Exception Handlers
register_error_handlers(app)

# 2. Attach Middlewares (Executed in reverse order of registration)
app.add_middleware(LoggingMiddleware)
app.add_middleware(RateLimitingMiddleware)
app.add_middleware(SecurityHeadersMiddleware)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RequestIdMiddleware)

# 3. Mount API Routers
app.include_router(auth_router, prefix="/api")
app.include_router(users_router, prefix="/api")
app.include_router(health_router, prefix="/api")


@app.get("/")
async def root():
    """Fallback root route indicating service status."""
    return {"message": "Atlas AI API", "status": "online"}
