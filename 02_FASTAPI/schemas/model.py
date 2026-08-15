from pydantic import BaseModel, ConfigDict
from typing import Literal


#Base model for the Model schema
class ModelBase(BaseModel):
    name: str
    provider: str
    category: Literal["llm", "embedding", "reranker"]


#Model creation schema
class ModelCreate(ModelBase):
    pass

#Model response schema
class ModelResponse(ModelBase):
    id: int


#Model update schema
class ModelUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = None
    provider: str | None = None
    category: Literal["llm", "embedding", "reranker"] | None = None



#Model replace schema
class ModelReplace(ModelBase):
    model_config = ConfigDict(extra="forbid")
