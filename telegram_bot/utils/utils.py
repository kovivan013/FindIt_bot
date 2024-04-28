import requests
import jwt

from datetime import datetime
from common.interfaces import OAuthStructure
from config import settings


def timestamp() -> int:
    return int(
        datetime.now().timestamp()
    )


class OAuth2:

    __SECRET_KEY: str = settings.SECRET_KEY

    @classmethod
    async def _prepare_token(
            cls,
            auth: int
    ) -> str:
        request = OAuthStructure(
            id_=auth,
            exp=timestamp() + 60
        )

        return jwt.encode(
            request.model_dump(),
            cls.__SECRET_KEY,
            algorithm="HS256"
        )

