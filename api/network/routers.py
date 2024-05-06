from fastapi import APIRouter
from .endpoints.debug import debug_router
from .endpoints.admin import admin_router
from .endpoints.user import user_router
from .endpoints.announcement import announcement_router


api_router = APIRouter()

api_router.include_router(
    debug_router,
    prefix="/debug",
    tags=["Debug"]
)
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
api_router.include_router(
    announcement_router,
    prefix="/announcements",
    tags=["Announcements"]
)

