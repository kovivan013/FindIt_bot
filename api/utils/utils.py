import hashlib
import jwt

from datetime import datetime
from uuid import uuid4
from starlette import status
from fastapi import (
    Request,
)
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from typing import Union

from config import settings
# from network.endpoints.admin import check_admin
from database.models.models import (
    Admins,
    Users,
    Announcements
)
from services.errors_reporter import Reporter
from services import exceptions
from schemas.base import (
    DataStructure,
    OAuthStructure
)


def timestamp() -> int:
    return int(
        datetime.now().timestamp()
    )

def _uuid() -> str:
    return str(
        uuid4()
    )

def _hash(string: str) -> str:
    hash = hashlib.sha384()
    hash.update(
        bytes(
            string,
            "utf-8"
        )
    )
    return hash.hexdigest()


class OAuth2:

    __SECRET_KEY: str = settings.SECRET_KEY

    @classmethod
    async def __get_token(
            cls,
            request: Request
    ) -> Union[OAuthStructure]:
        token = request.headers.get(
            "Authorization",
            None
        )

        if token is not None:
            try:
                result = OAuthStructure().model_validate(
                    jwt.decode(
                        token,
                        cls.__SECRET_KEY,
                        algorithms=['HS256']
                    )
                )

                return result
            except:
                raise exceptions.UnautorizedException
        raise exceptions.UnautorizedException

    @classmethod
    async def _check_admin(
            cls,
            request: Request,
            session: AsyncSession,
    ) -> Union[DataStructure]:
        result = DataStructure()
        token = await cls.__get_token(request)

        admin = await session.get(
            Admins,
            token.id_
        )

        if not admin:
            return await Reporter(
                exception=exceptions.NoAccess,
                message="Admin permissions required"
            )._report()

        await session.close()

        result.data = admin.as_dict()
        result._status = status.HTTP_200_OK

        return result

    @classmethod
    async def _check_token(
            cls,
            request: Request,
            session: AsyncSession,
            admin_permissions: bool = False
    ) -> Union[DataStructure, True]:
        token = await cls.__get_token(request)

        if admin_permissions:
            is_admin = await cls._check_admin(
                request,
                session
            )

            if not is_admin.success:
                raise exceptions.UnautorizedException
        return True

    @classmethod
    async def _check_ownership(
            cls,
            telegram_id: int,
            request: Request
    ) -> Union[DataStructure, True]:
        token = await cls.__get_token(request)

        if token.id_ == telegram_id:
            return True

        raise exceptions.NoAccess



# import jwt
#
#
# class OAuthSettings(BaseSettings):
#
#     model_config = SettingsConfigDict(
#         env_file=".env",
#         env_file_encoding="utf-8",
#         case_sensitive=False
#     )
#
#     __SECRET_KEY: str
#
#     @classmethod
#     async def _check_token(
#             cls,
#             request: Request,
#             _id: int
#     ) -> Union[DataStructure]:
#         token = request.headers.get(
#             "Authorization",
#             None
#         )
#         error = Reporter(
#             exception=exceptions.Unautorized
#         )
#
#         try:
#             decrypted_data = OAuthStructure().model_validate(
#                 jwt.decode(
#                     token,
#                     cls.__SECRET_KEY,
#                     algorithms=['HS256']
#                 )
#             )
#
#             if decrypted_data._id != _id:
#                 raise
#
#         except:
#             raise error._report()
#
#
#
#
#
#
# import datetime
#
# payload = {
#     'user_id': 123,
#     'exp': 1711989000
# }
# secret_key = 'your_secret_key'
# print(type(payload["exp"]))
# token = jwt.encode(payload, secret_key, algorithm='HS256')
# print(token)
# decoded_payload = jwt.decode(token, f"{secret_key}", algorithms=['HS256'])
# print(decoded_payload)

