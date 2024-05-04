import jwt

from datetime import datetime
from typing import Union
from pydantic import BaseModel
from common.interfaces import OAuthStructure
from aiogram.dispatcher.storage import FSMContext
from utils.utils import timestamp
from config import settings


class OAuth2:

    __SECRET_KEY: str = settings.SECRET_KEY

    @classmethod
    async def _prepare_token(
            cls,
            auth: int
    ) -> str:
        request = OAuthStructure(
            id_=auth,
            exp=timestamp() + 60
        )

        return jwt.encode(
            request.model_dump(),
            cls.__SECRET_KEY,
            algorithm="HS256"
        )


class FSMStorageProxy:

    def __init__(
            self,
            state: FSMContext
    ):
        self.state = state

    def __collect_path(
            self,
            path: str
    ) -> list:
        return [i for i in path.split("/") if i]

    async def get_data(
            self,
            path: str
    ) -> dict:
        keys = self.__collect_path(path)
        result: dict = {}

        async with self.state.proxy() as session:
            for i in keys:
                result = session.setdefault(
                    i, {}
                )

        return result

    async def data_model(
            self,
            path: str,
            model: BaseModel
    ) -> Union[BaseModel]:
        return model().model_validate(
            await self.get_data(path)
        )

    async def update_data(
            self,
            path: str,
            /,
            **kwargs
    ) -> dict:
        keys = self.__collect_path(path)
        update_path: dict = {}

        async with self.state.proxy() as session:
            default = session
            for i in keys:
                default = default.get(
                    i, {}
                )

            default.update(
                kwargs
            )

            update_path.update({
                keys[-1]: default
            })

            for i in reversed(keys[:-1]):
                update_path = {
                    i: update_path
                }

            session.update(
                update_path
            )

        return kwargs

    async def clear_partial_data(
            self,
            path: str
    ) -> None:
        keys = self.__collect_path(path)

        async with self.state.proxy() as session:
            update_path: dict = {}

            for i in keys:
                update_path = {
                    i: update_path
                }

                session.update(
                    update_path
                )






