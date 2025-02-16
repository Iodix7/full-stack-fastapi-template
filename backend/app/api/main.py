from fastapi import APIRouter

from app.api.routes import items, login, private, users, utils, customers  # Assicurati che customers sia importato
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)
api_router.include_router(items.router)
api_router.include_router(customers.router, prefix="/customers", tags=["customers"])  # Assicurati che il router di customers sia incluso

if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)