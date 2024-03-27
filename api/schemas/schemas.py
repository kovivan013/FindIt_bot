from typing import Optional, Dict, Any
from pydantic import BaseModel


class BaseUser(BaseModel):

    telegram_id: int = None
    username: str = None
    description: str = None
    badges: Dict[str, Any] = None
    phone_number: int = None
    mode: int = None
    announcements: Dict[str, Any] = None
    created_at: int = None
    updated_at: int = None


class BaseAnnouncement(BaseModel):

    announcement_id: str = None
    owner_id: int = None
    mode: int = None
    status: int = None
    details: Dict[str, Any] = None