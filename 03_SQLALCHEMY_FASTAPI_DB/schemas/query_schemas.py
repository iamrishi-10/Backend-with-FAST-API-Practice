from datetime import datetime

from pydantic import BaseModel, ConfigDict


class QueryCreate(BaseModel):
    project_id: int
    query_text: str
    answer_text: str | None = None


class QueryReplace(BaseModel):
    project_id: int
    query_text: str
    answer_text: str | None


class QueryUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # query_text is NOT NULL: `None` default only allows omission, not an
    # explicit `null` (still rejected by validation).
    query_text: str = None
    # answer_text IS nullable, so `str | None` correctly allows an explicit
    # `null` as a real, intentional value.
    answer_text: str | None = None


class QueryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    query_id: int
    project_id: int
    query_text: str
    answer_text: str | None
    created_at: datetime
