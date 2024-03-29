from fastapi import (
    APIRouter,
    Depends,
    Response,
    Request,
    Query
)
from typing import Union, Any
from starlette import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from .endpoints.user import (
    user_router,
    CreateUser
)
from .endpoints.admin import (
    admin_router
)

from database.core import (
    core,
    Endpoints
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


class UserMethods:

    @staticmethod
    @user_router.post(Endpoints.CREATE_USER)
    async def create_user(
            parameters: UserCreate,
            session: AsyncSession = Depends(
                core.create_sa_session
            )
    ) -> Union[DataStructure]:
        return await CreateUser(
            parameters=parameters,
            session=session
        )

class AdminMethods:
    pass
