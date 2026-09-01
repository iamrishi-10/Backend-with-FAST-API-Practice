from fastapi import APIRouter, Depends

from db.orm_models.user import User
from dependencies.auth import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/me")
def read_current_user(current_user: User = Depends(get_current_user)):
    return {
        "user_id": current_user.user_id,
        "email": current_user.email,
        "name": current_user.name,
    }
