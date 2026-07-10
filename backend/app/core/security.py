from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional
from jose import jwt  # Wait! PyJWT was installed, not jose! Let's check which JWT was installed.
# Ah, pyproject.toml has pyjwt. PyJWT is imported as: import jwt.
# Let's use jwt (PyJWT) which is import jwt, and has jwt.encode, jwt.decode.
import jwt
from passlib.context import CryptContext
from loguru import logger
from app.core.config import settings

# Setup password crypt context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain text password against a stored hash."""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        logger.error(f"Password verification error: {e}")
        return False


def get_password_hash(password: str) -> str:
    """Generates a secure password hash from a plain text password."""
    return pwd_context.hash(password)


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Generates an encrypted JWT access token containing the provided payload."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Decodes and validates a JWT token, returning the payload if valid."""
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        logger.debug("JWT token signature expired.")
        return None
    except jwt.InvalidTokenError as e:
        logger.debug(f"Invalid JWT token signature: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected JWT decode failure: {e}")
        return None
