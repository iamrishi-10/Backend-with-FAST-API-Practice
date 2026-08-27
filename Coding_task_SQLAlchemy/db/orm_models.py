from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Identity, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base


class Member(Base):
    __tablename__ = "members"

    member_id: Mapped[int] = mapped_column(Identity(), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    loans: Mapped[list["Loan"]] = relationship(
        back_populates="member", cascade="all, delete-orphan", passive_deletes=True
    )


class Book(Base):
    __tablename__ = "books"

    book_id: Mapped[int] = mapped_column(Identity(), primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    author: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    loans: Mapped[list["Loan"]] = relationship(
        back_populates="book", cascade="all, delete-orphan", passive_deletes=True
    )


class Loan(Base):
    __tablename__ = "loans"

    loan_id: Mapped[int] = mapped_column(Identity(), primary_key=True)
    member_id: Mapped[int] = mapped_column(
        ForeignKey("members.member_id", ondelete="CASCADE"), nullable=False
    )
    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.book_id", ondelete="CASCADE"), nullable=False
    )
    borrowed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    returned_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    member: Mapped["Member"] = relationship(back_populates="loans")
    book: Mapped["Book"] = relationship(back_populates="loans")
