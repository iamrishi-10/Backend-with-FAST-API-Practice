from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db.database import get_db
from schemas.books_schemas import BookCreate, BookResponse
from services import books_service

router = APIRouter(
    prefix='/books',
    tags=['books']
)


@router.post('/', response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    new_book = books_service.create_book(db, book)
    db.commit()
    return new_book
