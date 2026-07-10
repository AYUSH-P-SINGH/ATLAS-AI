from typing import Optional
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger
from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, decode_access_token
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate

# OAuth2 scheme for Swagger UI documentation
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login", auto_error=False)


class AuthService:
    @staticmethod
    async def register(db: AsyncSession, user_in: UserCreate) -> User:
        """Validates uniqueness of credentials and inserts the user."""
        # Check email uniqueness
        existing_email = await UserRepository.get_by_email(db, user_in.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists."
            )
        
        # Check username uniqueness
        existing_username = await UserRepository.get_by_username(db, user_in.username)
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this username already exists."
            )
        
        # Hash password and create user
        password_hash = get_password_hash(user_in.password)
        user = await UserRepository.create(db, user_in, password_hash)
        logger.info(f"User {user.username} registered successfully.")
        return user

    @staticmethod
    async def authenticate(db: AsyncSession, username_or_email: str, password: str) -> User:
        """Verifies plain credentials against db record by username or email."""
        # Find user by username or email
        if "@" in username_or_email:
            user = await UserRepository.get_by_email(db, username_or_email)
        else:
            user = await UserRepository.get_by_username(db, username_or_email)
            
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username/email or password.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user


async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db),
    token_from_header: Optional[str] = Depends(oauth2_scheme)
) -> User:
    """Dependency to extract user JWT token from cookies or headers and return current user."""
    token = None
    
    # 1. Attempt retrieval from cookie
    cookie_token = request.cookies.get("access_token")
    if cookie_token:
        # In case the cookie starts with 'Bearer ', slice it
        if cookie_token.startswith("Bearer "):
            token = cookie_token[7:]
        else:
            token = cookie_token
            
    # 2. Fallback to authorization header
    if not token and token_from_header:
        token = token_from_header

    # 3. Fallback to raw authorization header parse
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header[7:]

    # Throw unauthorized if token not resolved
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials not found.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Decode and validate payload
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id_str = payload.get("sub")
    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Malformed authentication credentials token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        import uuid
        user_id = uuid.UUID(user_id_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credential token format.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await UserRepository.get_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User associated with this token does not exist.",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    return user
