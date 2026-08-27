from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LoanCreate(BaseModel):
    member_id: int
    book_id: int


class LoanUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # returned_at IS nullable, so `datetime | None` correctly allows an
    # explicit `null` as a real value, distinct from omitting the field.
    returned_at: datetime | None = None


class LoanResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    loan_id: int
    member_id: int
    book_id: int
    borrowed_at: datetime
    returned_at: datetime | None
