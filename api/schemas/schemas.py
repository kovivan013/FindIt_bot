from typing import Optional, Dict, Any
from pydantic import BaseModel


class BaseUser(BaseModel):

    telegram_id: int = 0
    username: str = ""
    description: str = ""
    badges: Dict[str, Any] = {}
    phone_number: int = 0
    mode: int = 0
    announcements: Dict[str, Any] = {}
    created_at: int = 0
    notifications: Dict[str, Any] = {}


class BaseAnnouncement(BaseModel):

    announcement_id: str = ""
    owner_id: int = 0
    mode: int = 0
    status: int = 0
    details: Dict[str, Any] = {}
