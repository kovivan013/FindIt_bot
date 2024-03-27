from typing import Optional
from .base import Base
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
    announcements: Mapped[JSON] = mapped_column(
        JSON,
        default={}
    )
    created_at: Mapped[BigInteger] = mapped_column(
        BigInteger
    )
    notifications: Mapped[JSON] = mapped_column(
        JSON,
        default={}
    )


class Announcements(Base):

    announcements_id: Mapped[String] = mapped_column(
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