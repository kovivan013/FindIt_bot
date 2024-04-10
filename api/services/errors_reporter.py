from fastapi import FastAPI, Request
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
    def _exception(
            request: Request,
            exception: HTTPException
    ) -> JSONResponse:
        result = DataStructure()
        result._status = exception.status_code
        result.message = exception.detail
        return JSONResponse(status_code=result.status,
                            content=result.model_dump())

    @classmethod
    def start(
            cls,
            app: FastAPI
    ) -> None:

        app.add_exception_handler(
            status.HTTP_401_UNAUTHORIZED,
            cls._exception
        )
        app.add_exception_handler(
            status.HTTP_403_FORBIDDEN,
            cls._exception
        )

        # @app.exception_handler(RequestValidationError)
        # async def wrapper(
        #         *args: Any,
        #         **kwargs: Any
        # ) -> Union[JSONResponse]:
        #     result = DataStructure()
        #     result._status = status.HTTP_422_UNPROCESSABLE_ENTITY
        #     result.message = "Validation error"
        #     return JSONResponse(status_code=result.status,
        #                         content=result.model_dump())
