from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.database import get_db
from schemas.loan_schemas import LoanCreate, LoanResponse, LoanUpdate
from services import books_service, loan_service, member_service

router = APIRouter(
    prefix='/loans',
    tags=['loans']
)


@router.post('/', response_model=LoanResponse, status_code=status.HTTP_201_CREATED)
def create_loan(loan: LoanCreate, db: Session = Depends(get_db)):
    member = member_service.get_member_by_id(db, loan.member_id)
    if member is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Member not found')

    book = books_service.get_book_by_id(db, loan.book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')

    new_loan = loan_service.create_loan(db, loan)
    db.commit()
    return new_loan


@router.patch('/{loan_id}', response_model=LoanResponse)
def update_loan(loan_id: int, loan_data: LoanUpdate, db: Session = Depends(get_db)):
    loan = loan_service.get_loan_by_id(db, loan_id)

    if loan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Loan not found')

    updated_loan = loan_service.update_loan(db, loan, loan_data)
    db.commit()
    return updated_loan
