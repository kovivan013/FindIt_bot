from typing import Optional
from .base import Base
from pydantic import BaseModel

from schemas.schemas import (
    BaseUser,
    BaseAnnouncement
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
    DateTime
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
    phone_number: Mapped[Optional[BigInteger]] = mapped_column(
        BigInteger,
        default=0
    )
    mode: Mapped[SmallInteger] = mapped_column(
        SmallInteger
    )
    created_at: Mapped[BigInteger] = mapped_column(
        BigInteger,
        default=0
    )
    notifications: Mapped[JSON] = mapped_column(
        JSON,
        default={}
    )
    status: Mapped[SmallInteger] = mapped_column(
        SmallInteger,
        default=0
    )

    def as_model(self):
        return BaseUser().model_validate(
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
    details: Mapped[JSON] = mapped_column(
        JSON,
        default={}
    )

    def as_model(self):
        return BaseAnnouncement().model_validate(
            self.as_dict()
        )


class Admins(Base):

    telegram_id: Mapped[BigInteger] = mapped_column(
        BigInteger,
        primary_key=True,
        index=True
    )
    permissions: Mapped[JSON] = mapped_column(
        JSON,
        default={}
    )