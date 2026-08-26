from sqlalchemy import select
from sqlalchemy.orm import Session

from db.orm_models import User
from schemas.user_schemas import UserCreate, UserUpdate


def create_user(db: Session, user_data: UserCreate) -> User:
    new_user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
    )

    db.add(new_user)
    db.flush()
    db.refresh(new_user)

    return new_user


def get_all_users(db: Session) -> list[User]:
    return db.scalars(select(User)).all()


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)


def update_user(db: Session, user: User, user_data: UserUpdate) -> User:
    for field, value in user_data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)

    db.flush()
    db.refresh(user)

    return user


def replace_user(db: Session, user: User, user_data: UserCreate) -> User:
    user.first_name = user_data.first_name
    user.last_name = user_data.last_name
    user.email = user_data.email

    db.flush()
    db.refresh(user)

    return user


def delete_user(db: Session, user: User) -> None:
    db.delete(user)
    db.flush()
