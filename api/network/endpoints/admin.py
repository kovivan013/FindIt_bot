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

admin_router = APIRouter()