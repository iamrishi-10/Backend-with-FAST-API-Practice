from fastapi import FastAPI
from Routes.user_routes import router as users_router
from Routes.project_routes import router as projects_router
from Routes.query_routes import router as queries_router

app = FastAPI()

app.include_router(users_router)
app.include_router(projects_router)
app.include_router(queries_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Model API!"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}



