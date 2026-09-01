from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from core.config import GOOGLE_REDIRECT_URI
from core.security import create_access_token
from db.database import get_db
from services.auth_identity_service import get_or_create_oauth_user
from services.google_oauth import oauth

router = APIRouter(
    prefix="/auth/google",
    tags=["google-auth"],
)

@router.get("/login")
async def login(request: Request):
    return await oauth.google.authorize_redirect(
        request,
        GOOGLE_REDIRECT_URI,
    )

@router.get("/callback")
async def google_callback(
    request: Request,
    db: Session = Depends(get_db),
):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get("userinfo")

    if user_info is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google did not return user info",
        )

    user = get_or_create_oauth_user(
        db,
        provider="google",
        user_info=user_info,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google account is missing required or verified user info",
        )

    db.commit()
    db.refresh(user)

    access_token = create_access_token({"sub": str(user.user_id)})

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
