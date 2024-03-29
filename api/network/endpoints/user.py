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
    core,
)
from database.models.models import Users
from common.dto.user import (
    UserCreate,
    UserUpdate
)
from schemas.schemas import (
    BaseUser,
    BaseAnnouncement
)
from services import exceptions
from schemas.base import DataStructure
from utils import utils


user_router = APIRouter()


async def CreateUser(
        parameters: UserCreate,
        session: AsyncSession
) -> Union[DataStructure]:
    result = DataStructure()
    data_schema = BaseUser().model_validate(
        parameters.model_dump()
    )
    user_exist = await session.execute(
        select(
            Users.telegram_id
        ).filter(
            Users.telegram_id == data_schema.telegram_id
        )
    )

    if user_exist.scalars().all():
        # API REPORTER
        return result

    data_schema.created_at = utils.timestamp()
    session.add(
        Users(
            **data_schema.model_dump()
        )
    )
    await session.commit()
    await session.close()

    result.data = data_schema.model_dump()
    result._status = status.HTTP_201_CREATED

    return result

