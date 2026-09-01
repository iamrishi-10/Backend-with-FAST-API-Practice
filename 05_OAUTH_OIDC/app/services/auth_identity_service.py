from sqlalchemy import select
from sqlalchemy.orm import Session

from db.orm_models.auth_identity import AuthIdentity
from db.orm_models.user import User


def get_auth_identity(db: Session, provider: str, provider_subject: str) -> AuthIdentity | None:
    return db.scalars(
        select(AuthIdentity).where(
            AuthIdentity.provider == provider,
            AuthIdentity.provider_subject == provider_subject,
        )
    ).one_or_none()


def get_or_create_oauth_user(db: Session, provider: str, user_info: dict) -> User | None:
    provider_subject = user_info["sub"]

    identity = get_auth_identity(db, provider, provider_subject)

    if identity is not None:
        return identity.user

    email = user_info.get("email")
    name = user_info.get("name")

    if not email or not name:
        return None

    if user_info.get("email_verified") is not True:
        return None

    new_user = User(
        email=email,
        name=name,
    )

    db.add(new_user)
    db.flush()
    db.refresh(new_user)

    new_identity = AuthIdentity(
        user_id=new_user.user_id,
        provider=provider,
        provider_subject=provider_subject,
        provider_email=email,
    )

    db.add(new_identity)
    db.flush()

    return new_user
