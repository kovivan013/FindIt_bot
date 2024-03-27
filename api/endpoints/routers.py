from fastapi import APIRouter
from .v1.user_handlers import user_router
from .v1.admin_handlers import admin_router


api_router = APIRouter()

api_router.include_router(
    admin_router,
    prefix="/admin",
    tags=["Admin"]
)
api_router.include_router(
    user_router,
    prefix="/user",
    tags=["User"]
)
