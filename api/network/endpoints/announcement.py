from fastapi import (
    APIRouter,
    Depends,
    Response,
    Request,
    Query
)
from datetime import datetime
from typing import Union, AsyncIterable
from starlette import status
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
    BaseAnnouncement
)
from schemas.classes import (
    Endpoints,
    Status
)
from services import exceptions
from services.errors_reporter import Reporter
from schemas.base import DataStructure
from utils import utils


announcement_router = APIRouter()


@announcement_router.get(Endpoints.GET_ANNOUNCEMENT)
async def get_announcement(
        announcement_id: str,
        session: AsyncSession = Depends(
            core.create_sa_session
        )
) -> Union[DataStructure]:
    result = DataStructure()
    announcement = await session.get(
        Announcements,
        announcement_id
    )

    if not announcement:
        return await Reporter(
            exception=exceptions.ItemNotFound,
            message="Announcement not fount"
        )._report()

    await session.close()

    result.data = announcement.as_dict()
    result._status = status.HTTP_200_OK

    return result

# TODO: remove telegram_id param when token OAuth will be added
@announcement_router.delete(Endpoints.DELETE_ANNOUNCEMENT)
async def delete_announcement(
        telegram_id: int,
        announcement_id: str,
        session: AsyncSession = Depends(
            core.create_sa_session
)) -> Union[DataStructure]:
    result = DataStructure()



    return result