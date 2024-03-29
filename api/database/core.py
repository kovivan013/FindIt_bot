from typing import (
    Any,
    AsyncIterable,
    Optional,
    Union,
    TypeVar,
    Generic,
    Type,
)
from config import settings
from schemas.base import DataStructure
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from abc import ABC, abstractmethod
from fastapi import Depends
from pydantic import BaseModel

SessionFactoryType = async_sessionmaker[AsyncSession]


class Core:

    __slots__ = (
        "url",
        "engine",
        "session_factory",
    )

    def __init__(self, url: str) -> None:
        self.url = url
        self.engine = None
        self.session_factory = None

    def create_sa_engine(self) -> AsyncEngine:
        self.engine = create_async_engine(
            self.url
        )
        return self.engine

    def create_sa_session_factory(self) -> SessionFactoryType:
        self.session_factory = async_sessionmaker(
            self.engine or self.create_sa_engine(),
            autoflush=False,
            expire_on_commit=False
        )
        return self.session_factory

    async def create_sa_session(self) -> AsyncIterable[AsyncSession]:
        async with self.session_factory() as session:
            yield session

core = Core(
    url=settings.url,
)

ResultType = TypeVar("ResultType", bound=Any)

#
# class BaseMethod(ABC, Generic[ResultType]):
#
#     __slots__ = ()
#
#     def __init__(
#             self,
#             *args: Any,
#             **kwargs: Any
#     ) -> None:
#         return
#
#     async def __call__(
#             self,
#             session = Depends(
#                 core.create_sa_session
#             ),
#             **kwargs):
#         return await self._handle(
#             session=session,
#             **kwargs
#         )
#
#     @abstractmethod
#     async def _handle(
#             self,
#             session: AsyncIterable[AsyncSession],
#             **kwargs: Any
#     ) -> Union[DataStructure]:
#         pass


class Endpoints:

    GET_USER: str = "/{telegram_id}"
    CREATE_USER: str = "/create_user"
    UPDATE_USER: str = "/{telegram_id}"
    GET_ANNOUNCEMENT: str = "/{telegram_id}/{announcement_id}"
    CREATE_ANNOUNCEMENT: str = "/{telegram_id}/create_announcement"
    DELETE_ANNOUNCEMENT: str = "/{telegram_id}/{announcement_id}"

