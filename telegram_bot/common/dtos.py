from pydantic import BaseModel
from .schemas import (
    AnnouncementDetails
)
from .classes import (
    AnnouncementSort
)
from typing import Optional, Dict


class CreateUserDTO(BaseModel):

    telegram_id: int = 0
    username: str = ""
    description: Optional[str] = ""
    phone_number: int = 0


class UpdateUserDTO(BaseModel):

    username: Optional[str] = ""
    description: Optional[str] = ""
    phone_number: Optional[int] = 0


class AddAnnouncementDTO(AnnouncementDetails):

    mode: int = 0


class GetUserAnnouncementsDTO(BaseModel):

    mode: int = 0
    status: int = 0
    limit: int = 1
    page: int = 0


class GetAnnouncementsDTO(BaseModel):

    query: str = ""
    location: str = "",
    mode: int = 0
    status: int = 0
    limit: int = 1
    page: int = 0
    start_from: str = AnnouncementSort.latest


class AddAdminDTO(BaseModel):

    permissions: Dict[str, bool] = {}


class UpdatePermissionsDTO(BaseModel):

    permissions: Dict[str, bool] = {}


class BanUserDTO(BaseModel):

    reason: str = ""
    duration: int = 0


class GetUsersDTO(BaseModel):

    limit: int = 1
    page: int = 0


class GetBannedUsersDTO(BaseModel):

    limit: int = 1
    page: int = 0


class GetAdminsDTO(BaseModel):

    limit: int = 1
    page: int = 0


class SendNotificationDTO(BaseModel):

    preview: str = ""
    text: str = ""
    markup_type: int = 0



