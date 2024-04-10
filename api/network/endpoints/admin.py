from fastapi import (
    APIRouter,
    Depends,
    Response,
    Request,
    Query,
)
from typing_extensions import Annotated
from datetime import datetime
from typing import Union, AsyncIterable
from starlette import status as HTTPStatus
from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from database.core import (
    core
)
from database.models.models import (
    Users,
    Announcements
)
from common.dto.user import (
    UserCreate,
    UserUpdate
)
from common.dto.announcement import (
    AddAnnouncement
)
from schemas.schemas import (
    BaseUser,
    BaseAnnouncement,
    UserAnnouncementsResponse
)
from schemas.classes import (
    AdminEndpoints,
    AnnouncementStatus,
    AnnouncementSort,
    UserMode
)
from services import exceptions
from services.errors_reporter import Reporter
from schemas.base import DataStructure
from utils import utils
from utils.utils import OAuth2


admin_router = APIRouter()

@admin_router.post(AdminEndpoints.ADD_ADMIN)
async def add_admin(
        telegram_id: int,
        request: Request,
        session: AsyncSession = Depends(
            core.create_sa_session
        )
) -> Union[DataStructure]:
    await OAuth2._check_token(
        request,
        session
    )

    result = DataStructure()

    return result

@admin_router.post(AdminEndpoints.BAN_USER)
async def ban_user(
        telegram_id: int,
        request: Request,
        session: AsyncSession = Depends(
            core.create_sa_session
        )
) -> Union[DataStructure]:
    await OAuth2._check_token(
        request,
        session
    )

    result = DataStructure()

    return result

@admin_router.post(AdminEndpoints.ACCEPT_ANNOUNCEMENT)
async def accept_announcement(
        announcement_id: str,
        request: Request,
        session: AsyncSession = Depends(
            core.create_sa_session
        )
) -> Union[DataStructure]:
    await OAuth2._check_token(
        request,
        session
    )

    result = DataStructure()

    return result

@admin_router.post(AdminEndpoints.DECLINE_ANNOUNCEMENT)
async def decline_announcement(
        announcement_id: str,
        request: Request,
        session: AsyncSession = Depends(
            core.create_sa_session
        )
) -> Union[DataStructure]:
    await OAuth2._check_token(
        request,
        session
    )

    result = DataStructure()

    return result

@admin_router.post(AdminEndpoints.DELETE_ANNOUNCEMENT)
async def delete_announcement(
        announcement_id: str,
        request: Request,
        session: AsyncSession = Depends(
            core.create_sa_session
        )
) -> Union[DataStructure]:
    await OAuth2._check_token(
        request,
        session
    )

    result = DataStructure()

    return result