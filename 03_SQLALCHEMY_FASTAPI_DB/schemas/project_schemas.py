from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProjectCreate(BaseModel):
    user_id: int
    project_name: str
    status: str | None = None


class ProjectUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # Not `| None`: these columns are NOT NULL. The `None` default only
    # lets the field be omitted from the request (checked via
    # exclude_unset in update_project); an explicit `null` in the request
    # body still fails validation.
    project_name: str = None
    status: str = None


class ProjectReplace(BaseModel):
    user_id: int
    project_name: str
    status: str


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    project_id: int
    user_id: int
    project_name: str
    status: str
    created_at: datetime
