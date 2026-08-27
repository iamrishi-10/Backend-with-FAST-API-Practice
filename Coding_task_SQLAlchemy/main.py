from fastapi import FastAPI

from routes.member_routes import router as members_router
from routes.books_routes import router as books_router
from routes.loan_routes import router as loans_router

app = FastAPI()

app.include_router(members_router)
app.include_router(books_router)
app.include_router(loans_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Book Lending API!"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
