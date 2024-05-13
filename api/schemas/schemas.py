from typing import Optional, Dict, Any
from .classes import AnnouncementStatus
from pydantic import BaseModel


class BaseUser(BaseModel):

    telegram_id: int = 0
    username: str = ""
    description: str = ""
    badges: Dict[str, Any] = {}
    phone_number: str = "0"
    mode: int = 0
    created_at: int = 0
    is_banned: bool = False


class BannedUser(BaseModel):

    telegram_id: int = 0
    administrator: int = 0
    reason: str = ""
    banned_at: int = 0
    until: int = 0


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


class AnnouncementsResponse(BaseModel):

    query: str = ""
    page: int = 0
    pages: int = 0


class AnnouncementsOrder(BaseModel):

    active: int = 0
    completed: int = 0
    pending: int = 0


class UserAnnouncementsResponse(BaseModel):

    pages: int = 0
    page: int = 0
    status: int = AnnouncementStatus.ACTIVE
    order: AnnouncementsOrder = AnnouncementsOrder()


class BaseAnnouncement(AnnouncementDetails):

    announcement_id: str = ""
    owner_id: int = 0
    mode: int = 0
    status: int = 0


class AdminPermissions(BaseModel):

    SUPER_ADMIN: bool = False
    MANAGE_PERMISSIONS: bool = False
    MANAGE_ANNOUNCEMENTS: bool = False
    DELETE_ANNOUNCEMENTS: bool = False
    BAN_USERS: bool = False


class BaseAdmin(BaseModel):

    telegram_id: int = 0
    permissions: Dict[str, bool] = {}
    added_at: int = 0


class BaseNotification(BaseModel):

    id_: int = 0
    preview: str = ""
    text: str = ""
    unread: bool = True
    date: int = 0
    markup_type: int = 0


class UserNotifications(BaseModel):

    telegram_id: int = 0
    details: Dict[str, Any] = {}
    content: Dict[int, BaseNotification] = {}

