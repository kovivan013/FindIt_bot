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

