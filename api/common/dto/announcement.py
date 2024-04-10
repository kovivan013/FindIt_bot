from typing import Optional, Dict, Any
from schemas.schemas import AnnouncementDetails
from pydantic import BaseModel


class AddAnnouncement(AnnouncementDetails):

    mode: int = 0
