from fastapi import (
    APIRouter,
    Depends,
    Response,
    Request,
    Query
)
from starlette import status
from sqlalchemy.orm import Session

from database.core import core
from database.models.models import Users
# from common.dto.user import
# from schemas ...
from services import exceptions
# from services.errors_reporter import ...
from utils import utils

admin_router = APIRouter()