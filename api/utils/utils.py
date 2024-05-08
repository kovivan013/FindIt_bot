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
    BannedUsers,
    Users,
    Announcements
)
from services.errors_reporter import Reporter
from services import exceptions
from schemas.base import (
    DataStructure,
    OAuthStructure
)
from schemas.classes import ADMIN_PERMISSIONS


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
        """
        Decrypt secret JWT token. On success returns decrypted token structure.
        :param request:
        :return:
        """
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
            permissions: list,
            request: Request,
            session: AsyncSession,
    ) -> Union[DataStructure]:
        """
        Check is the user has admin permissions.
        :param permissions:
        :param request:
        :param session:
        :return:
        """
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

        for permission in permissions:
            if not admin.permissions.get(
                permission
            ) and not admin.permissions.get(
                ADMIN_PERMISSIONS.SUPER_ADMIN
            ) and admin.telegram_id not in settings.OWNERS:
                return await Reporter(
                    exception=exceptions.NoAccess,
                    message="Not enough permissions for this action"
                )._report()

        await session.close()

        result.data = admin.as_dict()
        result._status = status.HTTP_200_OK

        return result

    @classmethod
    async def _check_banned(
            cls,
            telegram_id: int,
            session: AsyncSession,
    ) -> Union[DataStructure]:
        result = DataStructure()

        banned_user = await session.get(
            BannedUsers,
            telegram_id
        )

        if not banned_user:
            result._status = status.HTTP_404_NOT_FOUND

            return result

        if banned_user.until <= timestamp():

            await session.delete(
                banned_user
            )
            await session.commit()

            result._status = status.HTTP_404_NOT_FOUND

            return result

        result.data = banned_user.as_dict()
        result._status = status.HTTP_200_OK

        return result

    @classmethod
    async def _check_token(
            cls,
            request: Request,
            session: AsyncSession,
            require_admin: bool = False,
            admin_permissions: list = []
    ) -> Union[DataStructure, OAuthStructure]:
        """
        Verify JWT token and required admin permissions to continue
        :param request:
        :param session:
        :param admin_permissions:
        :return:
        """
        token = await cls.__get_token(request)

        if admin_permissions or require_admin:
            is_admin = await cls._check_admin(
                admin_permissions,
                request,
                session
            )

            if not is_admin.success:
                raise exceptions.UnautorizedException
        return token

    @classmethod
    async def _check_new_admin_permissions(
            cls,
            permissions: list,
            request: Request,
            session: AsyncSession
    ) -> Union[DataStructure, True]:
        """
        Checks the admin has enough permissions to grant it towards new admin
        :param permissions: New admin permissions
        :param request:
        :param session:
        :return:
        """
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

        if admin.telegram_id in settings.OWNERS:
            permissions = []

        if ADMIN_PERMISSIONS.SUPER_ADMIN in permissions:
            if admin.telegram_id not in settings.OWNERS:
                return await Reporter(
                    exception=exceptions.NoAccess,
                    message="Not enought permissions"
                )._report()
            permissions = []

        for permission in permissions:
            if not admin.permissions.get(
                permission
            ) and not admin.permissions.get(
                ADMIN_PERMISSIONS.SUPER_ADMIN
            ):
                print(permission)
                return await Reporter(
                    exception=exceptions.NoAccess,
                    message="Not enough permissions for this action"
                )._report()

        await session.close()

        result.data = admin.as_dict()
        result._status = status.HTTP_200_OK

        return result

    @classmethod
    async def _check_ownership(
            cls,
            telegram_id: int,
            request: Request
    ) -> Union[DataStructure, True]:
        """
        Verify user is the author of the request
        :param telegram_id:
        :param request:
        :return:
        """
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

