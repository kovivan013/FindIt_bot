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
from utils.utils import OAuth2


user_router = APIRouter()


@user_router.post(Endpoints.CREATE_USER)
async def create_user(
        parameters: UserCreate,
        request: Request,
        session: AsyncSession = Depends(
            core.create_sa_session
        )
) -> Union[DataStructure]:
    # await OAuth2._check_token(
    #     request,
    #     UserCreate.telegram_id
    # )

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
    result._status = status.HTTP_201_CREATED

    return result


@user_router.get(Endpoints.GET_USER)
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

    data_scheme = BaseUser().model_validate(
        user.as_dict()
    )

    await session.close()

    result.data = data_scheme.model_dump()
    result._status = status.HTTP_200_OK

    return result


@user_router.patch(Endpoints.UPDATE_USER)
async def update_user(
        telegram_id: int,
        parameters: UserUpdate,
        request: Request,
        session: AsyncSession = Depends(
            core.create_sa_session
        )
) -> Union[DataStructure]:
    # await OAuth2._check_token(
    #     request,
    #     telegram_id
    # )

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

    result.data = user.as_dict()
    result._status = status.HTTP_200_OK

    return result


@user_router.post(Endpoints.ADD_ANNOUNCEMENT)
async def add_annoucement(
        telegram_id: int,
        parameters: AddAnnouncement,
        request: Request,
        session: AsyncSession = Depends(
            core.create_sa_session
        )
) -> Union[DataStructure]:
    # await OAuth2._check_token(
    #     request,
    #     telegram_id
    # )

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

    data_scheme = BaseAnnouncement().model_validate(
        parameters.model_dump()
    )
    data_scheme.owner_id = telegram_id
    data_scheme.announcement_id = utils._uuid()
    data_scheme.status = Status.PENDING

    session.add(
        Announcements(
            **data_scheme.model_dump()
        )
    )
    await session.commit()
    await session.close()

    result.data = data_scheme.model_dump()
    result._status = status.HTTP_201_CREATED

    return result
