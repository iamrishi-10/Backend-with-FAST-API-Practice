from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class UserUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # Not `| None`: these columns are NOT NULL. The `None` default only
    # lets the field be omitted from the request; it is never written to
    # the DB (update_user only applies fields present via exclude_unset).
    # An explicit `null` in the request body still fails validation.
    first_name: str = None
    last_name: str = None
    email: EmailStr = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    first_name: str
    last_name: str
    email: EmailStr
    created_at: datetime
