from fastapi import FastAPI

from routes.auth_routes import router as auth_router
from routes.user_routes import router as user_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)



@app.get("/")
def read_root():
    return {"message": "Welcome to the Book Lending API!"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}