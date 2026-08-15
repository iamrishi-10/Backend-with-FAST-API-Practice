from fastapi import APIRouter, HTTPException
from schemas.model import ModelCreate, ModelResponse, ModelUpdate, ModelReplace

router = APIRouter(
    prefix="/models",
    tags=["models"]
)

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

## Get all models with optional filtering by provider and category

@router.get("/")
def read_models(provider : str | None = None, category : str | None = None):
    results = MODELS

    if provider is not None:
        results = [model for model in results if model["provider"].lower() == provider.lower()]

    if category is not None:
        results = [model for model in results if model["category"].lower() == category.lower()]

    return {"models": results}




#Get a model by ID



@router.get("/{model_id}")
def read_model(model_id: int):
    for model in MODELS:
        if model["id"] == model_id:
            return model
    raise HTTPException(status_code=404, detail="Model not found")




#Create a new model

@router.post("/", response_model=ModelResponse, status_code=201)
def create_model(model: ModelCreate):
    next_id = max((m["id"] for m in MODELS), default=0) + 1

    new_model = model.model_dump()
    new_model["id"] = next_id

    MODELS.append(new_model)
    return new_model




#Update a model by ID

@router.patch("/{model_id}", response_model=ModelResponse)
def patch_model(model_id: int, updated_model: ModelUpdate):
    for model in MODELS:
        if model["id"] == model_id:
            model.update(updated_model.model_dump(exclude_unset=True))
            return model
    raise HTTPException(status_code=404, detail="Model not found")





#Replace a model by ID

@router.put("/{model_id}", response_model=ModelResponse)
def put_model(model_id: int, updated_model: ModelReplace):
    for model in MODELS:
        if model["id"] == model_id:
            model.update(updated_model.model_dump())
            return model
    raise HTTPException(status_code=404, detail="Model not found")




#Delete a model by ID

@router.delete("/{model_id}", status_code=204)
def delete_model(model_id: int):
    for index, model in enumerate(MODELS):
        if model["id"] == model_id:
            MODELS.pop(index)
            return
    raise HTTPException(status_code=404, detail="Model not found")