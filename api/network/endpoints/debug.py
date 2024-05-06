from fastapi import APIRouter
from typing import Union
from starlette import status as HTTPStatus
from schemas.base import DataStructure
from schemas.classes import DebugEndpoints


debug_router = APIRouter()

@debug_router.get(DebugEndpoints.HEALTH)
async def health() -> Union[DataStructure]:
    result = DataStructure()

    result._status = HTTPStatus.HTTP_200_OK

    return result

