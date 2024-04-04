from fastapi import (
    APIRouter,
    Depends,
    Response,
    Request,
    Query
)
from typing import Union, AsyncIterable
from starlette import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from database.core import (
    core,
)
from database.models.models import (
    Users,
    Announcements,
    Admins
)
from common.dto.user import (
    UserCreate,
    UserUpdate
)
from schemas.schemas import (
    BaseUser,
    BaseAnnouncement,
    BaseAdmin
)
from services import exceptions
from services.errors_reporter import Reporter
from schemas.base import DataStructure
from utils import utils
from utils.utils import OAuth2

admin_router = APIRouter()


# async def check_admin(
#         telegram_id: int,
#         session: AsyncSession
# ) -> Union[DataStructure]:
#     result = DataStructure()
#     admin = await session.get(
#         Admins,
#         telegram_id
#     )
#
#     if not admin:
#         return await Reporter(
#             exception=exceptions.NoAccess,
#             message="Admin permissions required"
#         )._report()
#
#     await session.close()
#
#     result.data = admin.as_dict()
#     result._status = status.HTTP_200_OK
#
#     return result