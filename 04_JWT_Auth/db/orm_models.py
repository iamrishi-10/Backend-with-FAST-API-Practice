from datetime import datetime

from sqlalchemy import Identity, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


class User(Base):
    __tablename__ = 'users'

    user_id : Mapped[int] = mapped_column(Identity(), primary_key=True)
    first_name : Mapped[str] = mapped_column(String(50), nullable = False)
    last_name : Mapped[str] = mapped_column(String(50), nullable = False)
    email : Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password_hash : Mapped[str] = mapped_column(String(255), nullable=False)
    created_at : Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )



