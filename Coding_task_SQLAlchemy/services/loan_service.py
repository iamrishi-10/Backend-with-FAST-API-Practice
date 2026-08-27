from sqlalchemy.orm import Session

from db.orm_models import Loan
from schemas.loan_schemas import LoanCreate, LoanUpdate


def create_loan(db:Session, loan_data: LoanCreate) -> Loan:
    new_loan = Loan(
        member_id = loan_data.member_id,
        book_id = loan_data.book_id
    )

    db.add(new_loan)
    db.flush()
    db.refresh(new_loan)

    return new_loan



def get_loan_by_id(db: Session, loan_id: int) -> Loan | None:
    return db.get(Loan, loan_id)



def update_loan(db: Session, loan: Loan, loan_data: LoanUpdate) -> Loan:
    for field, value in loan_data.model_dump(exclude_unset=True).items():
        setattr(loan, field, value)

    db.flush()
    db.refresh(loan)

    return loan
