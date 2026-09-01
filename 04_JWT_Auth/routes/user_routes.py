from fastapi import APIRouter, Depends

from db.orm_models import User
from schemas.user_schemas import UserResponse
from services.user_service import get_current_user

router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.get('/me', response_model=UserResponse)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user

