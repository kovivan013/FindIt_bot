import aiohttp

from schemas.schemas import DataStructure
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

    async def send_request(self) -> Union[DataStructure]:

        self._payload: dict = {
            "url": self.url
        }

        session_params: dict = {
            "trust_env": True,
            "connector": aiohttp.TCPConnector()
        }

        try:
            async with aiohttp.ClientSession(**session_params) as session:
                answer: ResponseStructure = await self._send(session)
        except Exception as err:
            raise Exception(err)

        # validate answer data
        result = DataStructure(**answer.data)
        result.data = answer.data["data"] if "data" in answer.data else answer.data

        # if answer.status not in range(200, 300):
        #     error_text: dict = {
        #         "status": answer.status,
        #         "url": self.url,
        #         "data": answer.data
        #     }
        #     return error_text
        return result

class GetRequest(RequestSender):
    def __init__(self, url: str = "", data: dict = None):
        super().__init__(url)
        self._data_for_send: dict = data
    async def _send(self, session) -> dict:
        self._payload.update(params=self._data_for_send)
        async with session.get(**self._payload) as response:
            return ResponseStructure(
                status=response.status,
                data=await response.json()
            )


class PostRequest(RequestSender):
    def __init__(self, url: str = "", data: dict = None):
        super().__init__(url)
        self._data_for_send: dict = data

    async def _send(self, session):
        self._payload.update(json=self._data_for_send)
        async with session.post(**self._payload) as response:
            return ResponseStructure(
                status=response.status,
                data=await response.json()
            )

class PatchRequest(RequestSender):
    def __init__(self, url: str = "", data: dict = None):
        super().__init__(url)
        self._data_for_send: dict = data

    async def _send(self, session):
        self._payload.update(json=self._data_for_send)
        async with session.patch(**self._payload) as response:
            return ResponseStructure(
                status=response.status,
                data=await response.json()
            )

class DeleteRequest(RequestSender):
    def __init__(self, url: str = "", data: dict = None):
        super().__init__(url)
        self._data_for_send: dict = data

    async def _send(self, session):
        self._payload.update(json=self._data_for_send)
        async with session.delete(**self._payload) as response:
            return ResponseStructure(
                status=response.status,
                data=await response.json()
            )