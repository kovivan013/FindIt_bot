import aiohttp

from common.interfaces import DataStructure, DataModel
from classes.utils_classes import OAuth2
from typing import Union
from abc import ABC, abstractmethod


class RequestSender(ABC):

    def __init__(
            self,
            url: str = ""
    ):
        self.url: str = url
        self._payload: dict = {}

    @abstractmethod
    async def _send(self):
        pass

    @classmethod
    async def _check_response(
            cls,
            response
    ) -> Union[DataStructure]:
        if response.status >= 500:

            return DataStructure(
                status=response.status,
                message="❌ Ой-ой.. Схоже виникла помилка.\n"
                        "Будь ласка, повторіть спробу!"
            )

        return DataStructure(
            **(await response.json())
        )

    async def send_request(
            self,
            auth: int
    ) -> Union[DataStructure]:

        self._payload: dict = {
            "url": self.url
        }

        headers: dict = {
            "Authorization": await OAuth2._prepare_token(
                auth
            )
        }

        session_params: dict = {
            "trust_env": True,
            "headers": headers,
            "connector": aiohttp.TCPConnector()
        }

        try:
            async with aiohttp.ClientSession(**session_params) as session:
                result: DataStructure = await self._send(
                    session
                )
        except Exception as err:

            return DataStructure(
                status=500,
                message="❌ Ой-ой.. Схоже виникла помилка.\n"
                        "Будь ласка, повторіть спробу!"
            )

        result.data = DataModel(
            result.data
        )

        return result

class GetRequest(RequestSender):

    def __init__(
            self,
            url: str = "",
            data: dict = None
    ):
        super().__init__(url)
        self._data_for_send: dict = data

    async def _send(
            self,
            session: aiohttp.ClientSession
    ) -> Union[DataStructure]:
        self._payload.update(
            params=self._data_for_send
        )
        async with session.get(**self._payload) as response:
            return await self._check_response(
                response
            )


class PostRequest(RequestSender):

    def __init__(
            self,
            url: str = "",
            data: dict = None
    ):
        super().__init__(url)
        self._data_for_send: dict = data

    async def _send(
            self,
            session: aiohttp.ClientSession
    ) -> Union[DataStructure]:
        self._payload.update(
            json=self._data_for_send
        )
        async with session.post(**self._payload) as response:
            return await self._check_response(
                response
            )


class PatchRequest(RequestSender):

    def __init__(
            self,
            url: str = "",
            data: dict = None
    ):
        super().__init__(url)
        self._data_for_send: dict = data

    async def _send(
            self,
            session: aiohttp.ClientSession
    ) -> Union[DataStructure]:
        self._payload.update(
            json=self._data_for_send
        )
        async with session.patch(**self._payload) as response:
            return await self._check_response(
                response
            )


class PutRequest(RequestSender):

    def __init__(
            self,
            url: str = "",
            data: dict = None
    ):
        super().__init__(url)
        self._data_for_send: dict = data

    async def _send(
            self,
            session: aiohttp.ClientSession
    ) -> Union[DataStructure]:
        self._payload.update(
            json=self._data_for_send
        )
        async with session.put(**self._payload) as response:
            return await self._check_response(
                response
            )


class DeleteRequest(RequestSender):

    def __init__(
            self,
            url: str = "",
            data: dict = None
    ):
        super().__init__(url)
        self._data_for_send: dict = data

    async def _send(
            self,
            session: aiohttp.ClientSession
    ) -> Union[DataStructure]:
        self._payload.update(
            json=self._data_for_send
        )
        async with session.delete(**self._payload) as response:
            return await self._check_response(
                response
            )


