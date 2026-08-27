from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session


from db.database import get_db
from schemas.loan_schemas import LoanResponse
from schemas.member_schemas import MemberCreate, MemberResponse
from services import member_service


router = APIRouter(
    prefix='/members',
    tags=['members']
)


@router.post('/', response_model=MemberResponse, status_code=status.HTTP_201_CREATED)
def create_member(member: MemberCreate, db: Session = Depends(get_db)):
    new_member = member_service.create_member(db, member)
    db.commit()
    return new_member


@router.get('/{member_id}/loans', response_model=list[LoanResponse])
def get_member_loans(member_id: int, db: Session = Depends(get_db)):
    member = member_service.get_member_by_id(db, member_id)

    if member is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Member not found')

    return member.loans