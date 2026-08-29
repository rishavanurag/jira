from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.organization import router as organization_router
from app.exceptions.handlers import register_exception_handlers

app = FastAPI(
    title="IAM Application",
    version="1.0.0"
)

register_exception_handlers(app)

app.include_router(auth_router)
app.include_router(organization_router)
