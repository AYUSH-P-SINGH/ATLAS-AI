from fastapi import APIRouter, Depends
from app.models.user import User
from app.schemas.user import UserOut
from app.services.auth import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserOut)
async def get_me(current_user: User = Depends(get_current_user)) -> User:
    """Returns the currently authenticated user profile."""
    return current_user
