from typing import Optional, Dict, Any
from schemas.schemas import AnnouncementDetails
from pydantic import BaseModel


class AddAnnouncement(BaseModel):

    mode: int = 0
    details: AnnouncementDetails = AnnouncementDetails()
