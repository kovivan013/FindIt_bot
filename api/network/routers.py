from fastapi import APIRouter
from .methods import (
    admin_router,
    user_router,
)


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
