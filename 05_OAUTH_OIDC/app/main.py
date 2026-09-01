from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from core.config import SESSION_SECRET
from routes.google_auth import router as google_auth_router
from routes.user_routes import router as user_router

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET,
)

app.include_router(google_auth_router)
app.include_router(user_router)
