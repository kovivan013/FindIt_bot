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
from sqlalchemy import (
    select,
    String
)
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
    AnnouncementsResponse
)
from schemas.classes import (
    AnnouncementEndpoints,
    AnnouncementStatus,
    AnnouncementSort,
)
from services import exceptions
from services.errors_reporter import Reporter
from schemas.base import DataStructure
from utils import utils
from utils.utils import OAuth2


announcement_router = APIRouter()


@announcement_router.get(AnnouncementEndpoints.GET_ANNOUNCEMENT)
async def get_announcement(
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

@announcement_router.delete(AnnouncementEndpoints.DELETE_ANNOUNCEMENT)
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
    announcement = await session.get(
        Announcements,
        announcement_id
    )

    if not announcement:
        return await Reporter(
            exception=exceptions.ItemNotFound,
            message="Announcement not fount"
        )._report()

    if announcement.status != AnnouncementStatus.ACTIVE:
        return await Reporter(
            exception=exceptions.NoAccess,
            message="Announcement cannot be deleted"
        )._report()

    await OAuth2._check_ownership(
        announcement.owner_id,
        request
    )

    await session.delete(
        announcement
    )

    await session.commit()
    await session.close()

    result.message = "Announcement successfully deleted"
    result._status = status.HTTP_200_OK

    return result

@announcement_router.get(AnnouncementEndpoints.GET_ANNOUNCEMENTS)
async def get_announcements(
        request: Request,
        query: str,
        location: str = "",
        limit: int = 1,
        page: int = 0,
        start_from: AnnouncementSort = Query(
            default=AnnouncementSort.latest
        ),
        session: AsyncSession = Depends(
            core.create_sa_session
        )
) -> Union[DataStructure]:
    # await OAuth2._check_token(
    #     request,
    #     session
    # )

    result = DataStructure()
    document = AnnouncementsResponse(
        query=query,
        page=page
    )

    query_result = await session.execute(
        select(
            Announcements
        ).filter(
            Announcements.status == AnnouncementStatus.ACTIVE
        ).filter(
            Announcements.title.ilike(
                f"%{query}%"
            )
        ).filter(
            (
                Announcements.location.op(
                    "->>"
                )(
                    "place_name"
                ).cast(
                    String
                ).ilike(
                    f"%{location}%"
                )
            ) if location else True
        ).order_by(
            Announcements.timestamp.desc() if start_from._value
            else Announcements.timestamp.asc()
        ).offset(
            page * limit
        ).limit(
            limit
        )
    )

    announcements: dict = {}

    for announcement in query_result.scalars().all():
        announcements.update(
            {
                announcement.announcement_id: announcement.as_dict()
            }
        )

    result.data.update(
        {
            "announcements": announcements,
            "document": document
        }
    )
    result._status = status.HTTP_200_OK

    return result