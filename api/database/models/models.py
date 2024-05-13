from typing import Optional, Union
from .base import Base
from pydantic import BaseModel

from schemas.schemas import (
    BaseUser,
    BaseAnnouncement,
    BaseAdmin,
    BannedUser
)
from sqlalchemy.orm import (
    mapped_column,
    Mapped
)
from sqlalchemy import (
    Column,
    Integer,
    String,
    BigInteger,
    JSON,
    SmallInteger,
    DateTime,
    ARRAY
)


class Users(Base):

    telegram_id: Mapped[BigInteger] = mapped_column(
        BigInteger,
        primary_key=True,
        index=True
    )
    username: Mapped[Optional[String]] = mapped_column(
        String,
        default=""
    )
    description: Mapped[Optional[String]] = mapped_column(
        String,
        default=""
    )
    badges: Mapped[JSON] = mapped_column(
        JSON,
        default={}
    )
    phone_number: Mapped[Optional[String]] = mapped_column(
        String,
        default="0"
    )
    mode: Mapped[SmallInteger] = mapped_column(
        SmallInteger
    )
    created_at: Mapped[BigInteger] = mapped_column(
        BigInteger,
        default=0
    )

    def as_model(self) -> Union[BaseUser]:
        return BaseUser().model_validate(
            self.as_dict()
        )


class BannedUsers(Base):

    telegram_id: Mapped[BigInteger] = mapped_column(
        BigInteger,
        primary_key=True,
        index=True
    )
    administrator: Mapped[BigInteger] = mapped_column(
        BigInteger
    )
    reason: Mapped[String] = mapped_column(
        String,
        default=""
    )
    banned_at: Mapped[BigInteger] = mapped_column(
        BigInteger,
        default=0
    )
    until: Mapped[BigInteger] = mapped_column(
        BigInteger,
        default=0
    )

    def as_model(self) -> Union[BannedUser]:
        return BannedUser().model_validate(
            self.as_dict()
        )


class Announcements(Base):

    announcement_id: Mapped[String] = mapped_column(
        String,
        primary_key=True,
        index=True
    )
    owner_id: Mapped[BigInteger] = mapped_column(
        BigInteger
    )
    mode: Mapped[SmallInteger] = mapped_column(
        SmallInteger
    )
    status: Mapped[SmallInteger] = mapped_column(
        SmallInteger,
        default=0
    )
    title: Mapped[String] = mapped_column(
        String,
        default=""
    )
    description: Mapped[String] = mapped_column(
        String,
        default=""
    )
    location: Mapped[JSON] = mapped_column(
        JSON,
        default={}
    )
    address: Mapped[JSON] = mapped_column(
        JSON,
        default={}
    )
    timestamp: Mapped[BigInteger] = mapped_column(
        BigInteger,
        default=0
    )
    tags: Mapped[ARRAY] = mapped_column(
        ARRAY(String),
        default=[]
    )
    secrets: Mapped[JSON] = mapped_column(
        JSON,
        default={}
    )

    def as_model(self) -> Union[BaseAnnouncement]:
        return BaseAnnouncement().model_validate(
            self.as_dict()
        )


class Admins(Base):

    telegram_id: Mapped[BigInteger] = mapped_column(
        BigInteger,
        primary_key=True,
        index=True
    )
    administrator: Mapped[BigInteger] = mapped_column(
        BigInteger
    )
    permissions: Mapped[JSON] = mapped_column(
        JSON,
        default={}
    )
    added_at: Mapped[BigInteger] = mapped_column(
        BigInteger,
        default=0
    )

    def as_model(self) -> Union[BaseAdmin]:
        return BaseAdmin().model_validate(
            self.as_dict()
        )


class Notifications(Base):

    telegram_id: Mapped[BigInteger] = mapped_column(
        BigInteger,
        primary_key=True,
        index=True
    )
    details: Mapped[JSON] = mapped_column(
        JSON,
        default={}
    )
    content: Mapped[JSON] = mapped_column(
        JSON,
        default={}
    )