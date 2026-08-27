from sqlalchemy.orm import Session

from db.orm_models import Member
from schemas.member_schemas import MemberCreate



def create_member(db:Session, member_data: MemberCreate) -> Member:
    new_member = Member(
        name = member_data.name,
        email = member_data.email
    )

    db.add(new_member)
    db.flush()
    db.refresh(new_member)

    return new_member



def get_member_by_id(db: Session, member_id: int) -> Member | None:
    return db.get(Member, member_id)

