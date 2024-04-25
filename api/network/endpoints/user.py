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
    UserEndpoints,
    AnnouncementStatus,
    AnnouncementSort,
    UserMode
)
from services import exceptions
from services.errors_reporter import Reporter
from schemas.base import DataStructure
from utils import utils
from utils.utils import OAuth2


user_router = APIRouter()


@user_router.post(UserEndpoints.CREATE_USER)
async def create_user(
        parameters: UserCreate,
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

    data_scheme = BaseUser().model_validate(
        parameters.model_dump()
    )
    user = await session.get(
        Users,
        parameters.telegram_id
    )

    if user:
        return await Reporter(
            exception=exceptions.ItemExists,
            message="User already exist"
        )._report()

    data_scheme.created_at = utils.timestamp()
    session.add(
        Users(
            **data_scheme.model_dump()
        )
    )
    await session.commit()
    await session.close()

    result.data = data_scheme.model_dump()
    result._status = HTTPStatus.HTTP_201_CREATED

    return result


@user_router.get(UserEndpoints.GET_USER)
async def get_user(
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

    user = await session.get(
        Users,
        telegram_id
    )

    if not user:
        return await Reporter(
            exception=exceptions.ItemNotFound,
            message="User not found"
        )._report()

    await session.close()

    result.data = user.as_model().model_dump()
    result._status = HTTPStatus.HTTP_200_OK

    return result


@user_router.patch(UserEndpoints.UPDATE_USER)
async def update_user(
        telegram_id: int,
        parameters: UserUpdate,
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

    user = await session.get(
        Users,
        telegram_id
    )

    if not user:
        return await Reporter(
            exception=exceptions.ItemNotFound,
            message="User not found"
        )._report()

    user.validate(
        parameters.model_dump(
            exclude_defaults=True
        )
    )
    await session.commit()
    await session.close()

    result.data = user.as_model().model_dump()
    result._status = HTTPStatus.HTTP_200_OK

    return result


@user_router.post(UserEndpoints.ADD_ANNOUNCEMENT)
async def add_annoucement(
        telegram_id: int,
        parameters: AddAnnouncement,
        request: Request,
        session: AsyncSession = Depends(
            core.create_sa_session
        )
) -> Union[DataStructure]:
    token = await OAuth2._check_token(
        request,
        session
    )
    result = DataStructure()

    if token.id_ != telegram_id:
        return await Reporter(
            exception=exceptions.NoAccess,
            message="Only the account owner have permissions to place the announcements"
        )

    user = await session.get(
        Users,
        telegram_id
    )

    if not user:
        return await Reporter(
            exception=exceptions.ItemNotFound,
            message="User not found"
        )._report()

    data_scheme = BaseAnnouncement().model_validate(
        parameters.model_dump()
    )
    data_scheme.owner_id = telegram_id
    data_scheme.announcement_id = utils._uuid()
    data_scheme.status = AnnouncementStatus.PENDING

    session.add(
        Announcements(
            **data_scheme.model_dump()
        )
    )
    await session.commit()
    await session.close()

    result.data = data_scheme.model_dump()
    result._status = HTTPStatus.HTTP_201_CREATED

    return result

@user_router.get(UserEndpoints.GET_USER_ANNOUNCEMENTS)
async def get_user_announcements(
        request: Request,
        telegram_id: int,
        mode: int = Query(
            0,
            gt=-1,
            lt=2
        ),
        status: int = Query(
            0,
            gt=-1,
            lt=3
        ),
        limit: int = Query(
            1,
            gt=0
        ),
        page: int = 0,
        session: AsyncSession = Depends(
            core.create_sa_session
        )
) -> Union[DataStructure]:
    await OAuth2._check_token(
        request,
        session
    )
    result = DataStructure()

    document = UserAnnouncementsResponse(
        status=status,
        page=page
    )
    query_result = await session.execute(
        select(
            Announcements
        ).filter(
            Announcements.owner_id == telegram_id
        ).filter(
            Announcements.mode == mode
        ).order_by(
            Announcements.timestamp.desc()
        )
    )

    announcements: dict = {}
    offset: int = page * limit

    for i, announcement in enumerate(query_result.scalars().all()):

        match announcement.status:
            case 0:
                document.order.active += 1
            case 1:
                document.order.completed += 1
            case 2:
                document.order.pending += 1

        if not i % limit:
            document.pages += 1

        if i in range(
                offset,
                offset + limit
        ):
            if announcement.status == status:
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
    result._status = HTTPStatus.HTTP_200_OK

    return result
