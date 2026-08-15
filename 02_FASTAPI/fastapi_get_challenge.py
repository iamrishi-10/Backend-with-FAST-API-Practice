from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
from typing import Literal

app = FastAPI()

MODELS = [
    {
        "id": 1,
        "name": "GPT-4.1",
        "provider": "OpenAI",
        "category": "llm",
    },
    {
        "id": 2,
        "name": "GPT-4.1 Mini",
        "provider": "OpenAI",
        "category": "llm",
    },
    {
        "id": 3,
        "name": "text-embedding-3-small",
        "provider": "OpenAI",
        "category": "embedding",
    },
    {
        "id": 4,
        "name": "text-embedding-3-large",
        "provider": "OpenAI",
        "category": "embedding",
    },
    {
        "id": 5,
        "name": "Claude Sonnet 4",
        "provider": "Anthropic",
        "category": "llm",
    },
    {
        "id": 6,
        "name": "Command R",
        "provider": "Cohere",
        "category": "llm",
    },
    {
        "id": 7,
        "name": "Cohere Embed",
        "provider": "Cohere",
        "category": "embedding",
    },
    {
        "id": 8,
        "name": "Cohere Rerank",
        "provider": "Cohere",
        "category": "reranker",
    },
]



@app.get("/")
def read_root():
    return {"message": "Welcome to the Model API!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

##Collection route + filter using query parameters
@app.get("/models")
def get_models(provider: str | None = None, category: str | None = None):
    results = MODELS

    if provider is not None:
        results = [m for m in results if m["provider"].lower() == provider.lower()]

    if category is not None:
        results = [m for m in results if m["category"].lower() == category.lower()]

    return {"models": results}


##Pagination-style query parameters
@app.get("/models/paginated")
def get_models_paginated(limit: int = 10, page: int = 1):
    start = (page - 1) * limit
    end = start + limit
    return {"models": MODELS[start:end], "limit": limit, "page": page}


##Individual model using a path parameter
@app.get("/models/{model_id}")
def get_model(model_id: int):
    for model in MODELS:
        if model["id"] == model_id:
            return {"model": model}
    raise HTTPException(status_code=404, detail="Model not found")


##Path parameter (provider) + query parameter (category) together
@app.get("/providers/{provider}/models")
def get_models_by_provider(provider: str, category: str | None = None):
    results = [m for m in MODELS if m["provider"].lower() == provider.lower()]

    if category is not None:
        results = [m for m in results if m["category"].lower() == category.lower()]

    return {"provider": provider, "category": category, "models": results}



# ##Post request
# @app.post("/models/create_model")
# def create_model(model: dict):
#     for existing_model in MODELS:
#         if existing_model["name"].lower() == model["name"].lower():
#             return {"message": "Model already exists, skipping", "model": existing_model}

#     model["id"] = len(MODELS) + 1
#     MODELS.append(model)
#     return {"message": "Model created successfully", "model": model}


# @app.put("/models/update_model/{model_id}")
# def update_model(model_id: int, updated_model: dict):
#     for model in MODELS:
#         if model["id"] == model_id:
#             model.update(updated_model)
#             return {"message": "Model updated successfully", "model": model}
#     raise HTTPException(status_code=404, detail="Model not found")


# @app.delete("/models/delete_model/{model_id}")
# def delete_model(model_id: int):
#     for index, model in enumerate(MODELS):
#         if model["id"] == model_id:
#             deleted_model = MODELS.pop(index)
#             return {"message": "Model deleted successfully", "model": deleted_model}
#     raise HTTPException(status_code=404, detail="Model not found")



# if __name__ == "__main__":
#     import requests

#     BASE_URL = "http://127.0.0.1:8000"

#     new_model = {
#         "name": "Gemini 2.5 Pro",
#         "provider": "Google",
#         "category": "llm",
#     }

#     response = requests.post(f"{BASE_URL}/models/create_model", json=new_model)

#     print("Status code:", response.status_code)
#     print("Response body:", response.json())

#     updated_model = {
#         "name": "Anthropic Embed",
#         "provider": "Anthropic",
#         "category": "embedding",
#     }

#     put_response = requests.put(f"{BASE_URL}/models/update_model/6", json=updated_model)

#     print("Status code:", put_response.status_code)
#     print("Response body:", put_response.json())


#     delete_response = requests.delete(f"{BASE_URL}/models/delete_model/7")
#     print("Status code:", delete_response.status_code)
#     print("Response body:", delete_response.json())



#  Post with Pydantic Validation

class ModelBase(BaseModel):
    name: str
    provider: str
    category: Literal["llm", "embedding", "reranker"]


class ModelCreate(ModelBase):
    pass


class ModelResponse(ModelBase):
    id: int


@app.post("/models", response_model=ModelResponse, status_code=201)
def create_model(model: ModelCreate):
    next_id = max((m["id"] for m in MODELS), default=0) + 1

    new_model = model.model_dump()
    new_model["id"] = next_id

    MODELS.append(new_model)
    return new_model


# Patch with Pydantic Validation

class ModelUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = None
    provider: str | None = None
    category: Literal["llm", "embedding", "reranker"] | None = None


@app.patch("/models/{model_id}", response_model=ModelResponse)
def patch_model(model_id: int, updated_model: ModelUpdate):
    for model in MODELS:
        if model["id"] == model_id:
            model.update(updated_model.model_dump(exclude_unset=True))
            return model
    raise HTTPException(status_code=404, detail="Model not found")


#Put with Pydantic Validation
class ModelReplace(ModelBase):
    model_config = ConfigDict(extra="forbid")


@app.put("/models/{model_id}", response_model=ModelResponse)
def put_model(model_id: int, updated_model: ModelReplace):
    for model in MODELS:
        if model["id"] == model_id:
            model.update(updated_model.model_dump())
            return model
    raise HTTPException(status_code=404, detail="Model not found")



#Delete with Pydantic Validation

@app.delete("/models/{model_id}", status_code=204)
def delete_model(model_id: int):
    for index, model in enumerate(MODELS):
        if model["id"] == model_id:
            MODELS.pop(index)
            return
    raise HTTPException(status_code=404, detail="Model not found")
