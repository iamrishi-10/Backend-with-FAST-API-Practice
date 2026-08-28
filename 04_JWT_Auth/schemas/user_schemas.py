from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    first_name: str
    last_name: str
    email: str
    created_at: datetime
