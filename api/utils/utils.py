import hashlib
import jwt

from datetime import datetime
from uuid import uuid4
from starlette import status
from fastapi import Request
from fastapi.responses import JSONResponse
from typing import Union

from config import settings
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
    async def _check_token(
            cls,
            request: Request,
            id_: int
    ) -> Union[DataStructure, None]:
        token = request.headers.get(
            "Authorization",
            None
        )

        try:
            decrypted_data = OAuthStructure().model_validate(
                jwt.decode(
                    token,
                    cls.__SECRET_KEY,
                    algorithms=['HS256']
                )
            )

            if decrypted_data.id_ != id_:
                raise

        except:
            raise exceptions.UnautorizedException


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

