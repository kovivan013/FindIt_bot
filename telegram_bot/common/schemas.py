from pydantic import BaseModel
from typing import Dict, Any


class BaseUser(BaseModel):

    telegram_id: int = 0
    username: str = ""
    description: str = ""
    badges: Dict[str, Any] = {}
    phone_number: int = 0
    mode: int = 0
    created_at: int = 0
    is_banned: bool = False
    notifications: Dict[str, Any] = {}
    status: int = 0


class BannedUser(BaseModel):

    telegram_id: int = 0
    administrator: int = 0
    reason: str = ""
    banned_at: int = 0
    until: int = 0


class BaseAdmin(BaseModel):

    telegram_id: int = 0
    permissions: Dict[str, bool] = {}
    added_at: int = 0


class AnnouncementLocation(BaseModel):

    latitude: float = 0.0
    longitude: float = 0.0
    place_name: str = ""
    place_type: str = ""


class AnnouncementSecrets(BaseModel):

    question: str = ""
    answer: str = ""


class AnnouncementDetails(BaseModel):

    title: str = ""
    description: str = ""
    address: Dict[str, Any] = {}
    timestamp: int = 0
    tags: list = []
    secrets: AnnouncementSecrets = AnnouncementSecrets()
    location: AnnouncementLocation = AnnouncementLocation()


class BaseAnnouncement(AnnouncementDetails):

    announcement_id: str = ""
    owner_id: int = 0
    mode: int = 0
    status: int = 0