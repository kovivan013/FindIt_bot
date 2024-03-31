from fastapi import FastAPI
from typing import Union, Any
from starlette import status

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

from schemas.base import DataStructure
from . import exceptions


class Reporter:

    def __init__(
            self,
            exception: HTTPException,
            message: str = ""
    ) -> None:
        self.exception = exception
        self.status = exception.status_code
        self.message = message or exception.detail

    async def _report(self) -> Union[DataStructure]:
        result = DataStructure().model_validate(
            vars(self)
        )
        result._status = self.status

        return result

    @staticmethod
    def start(app: FastAPI) -> None:

        @app.exception_handler(RequestValidationError)
        async def wrapper(
                *args: Any,
                **kwargs: Any
        ) -> Union[JSONResponse]:
            result = DataStructure()
            result._status = status.HTTP_422_UNPROCESSABLE_ENTITY
            result.message = "Validation error"
            return JSONResponse(status_code=result.status,
                                content=result.model_dump())
