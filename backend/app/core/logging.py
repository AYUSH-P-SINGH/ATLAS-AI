import sys
from loguru import logger
from app.core.config import settings


def setup_logging() -> None:
    """Configures system-wide structured logging utilizing Loguru."""
    # Clear any default configuration
    logger.remove()
    
    # Register custom stdout formatter
    logger.add(
        sys.stdout,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        ),
        level=settings.LOG_LEVEL.upper(),
        enqueue=True,  # Makes logging thread-safe and non-blocking
    )
    
    logger.info("Structured logging has been configured successfully.")
