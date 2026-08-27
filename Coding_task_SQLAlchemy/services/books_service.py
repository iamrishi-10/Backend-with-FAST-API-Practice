from sqlalchemy.orm import Session


from db.orm_models import Book
from schemas.books_schemas import BookCreate


def create_book(db: Session, book_data:BookCreate) -> Book:
    new_book = Book(
        title = book_data.title,
        author = book_data.author
    )

    db.add(new_book)
    db.flush()
    db.refresh(new_book)

    return new_book


def get_book_by_id(db: Session, book_id : int) -> Book | None:
    return db.get(Book, book_id)

