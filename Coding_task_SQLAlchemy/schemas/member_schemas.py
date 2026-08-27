from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class MemberCreate(BaseModel):
    name: str
    email: EmailStr


class MemberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    member_id: int
    name: str
    email: EmailStr
    created_at: datetime
