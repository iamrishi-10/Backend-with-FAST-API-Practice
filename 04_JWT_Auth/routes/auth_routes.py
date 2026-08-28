from fastapi import HTTPException, status, APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.security import create_access_token
from db.database import get_db
from schemas.auth_schemas import LoginRequest, SignupRequest, TokenResponse
from schemas.user_schemas import UserResponse
from services import auth_service


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@router.post('/signup', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(signup_data: SignupRequest, db: Session = Depends(get_db)):
    new_user = auth_service.signup_user(db, signup_data)

    if new_user is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email already registered')

    db.commit()
    return new_user


@router.post('/login', response_model=TokenResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(db, login_data)

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid email or password')

    access_token = create_access_token({"sub": str(user.user_id)})

    return TokenResponse(access_token=access_token, token_type="bearer")


@router.post('/token', response_model=TokenResponse)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    login_data = LoginRequest(email=form_data.username, password=form_data.password)
    user = auth_service.authenticate_user(db, login_data)

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid email or password')

    access_token = create_access_token({"sub": str(user.user_id)})

    return TokenResponse(access_token=access_token, token_type="bearer")
