from fastapi import FastAPI
from routes.models import router as models_router

app = FastAPI()

app.include_router(models_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Model API!"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}



