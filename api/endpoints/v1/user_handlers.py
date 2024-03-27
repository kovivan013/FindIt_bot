from fastapi import (
    APIRouter,
    Depends,
    Response,
    Request,
    Query
)
from starlette import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from database.core import core
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

@user_router.get("/endpoint")
async def create_user(value: int, session: AsyncSession = Depends(core.create_sa_session)):
    result = DataStructure()

    query = select(Users).filter(Users.telegram_id == value)

    response = await session.execute(query)
    partial_data = response.scalars().first()
    print(partial_data.as_dict())


    return result
    # user_exists = await session.query(Users).filter(Users.telegram_id == request_data.telegram_id).first()
    # if user_exists:
    #     return Reporter.api_exception(exception=exceptions.ItemExistsException,
    #                                   message="User already exists")
    #
    # data = BaseUser().model_validate(request_data.model_dump())
    # data.created_at = int(datetime.datetime.now().timestamp())
    #
    # result._status = status.HTTP_201_CREATED
    # result.data = data.model_dump()
    #
    # db.close()
    # return PostRequest(db=db,
    #                    response=response,
    #                    data=result.data,
    #                    result=result).send_request()
