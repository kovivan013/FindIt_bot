import jwt

from network.endpoints import (
    UserEndpoints,
    AnnouncementEndpoints,
    AdminEndpoints
)
from pydantic import BaseModel
from typing import Union
from schemas.schemas import DataStructure
from config import settings

class UserEndpoints:

    GET_USER: str = "/{telegram_id}"
    CREATE_USER: str = "/create_user"
    UPDATE_USER: str = "/{telegram_id}"
    ADD_ANNOUNCEMENT: str = "/{telegram_id}/add_announcement"
    GET_USER_ANNOUNCEMENTS: str = "/{telegram_id}/announcements"
    SEND_NOTIFICATION: str = "/{telegram_id}/send_notification"


class AnnouncementEndpoints:

    GET_ANNOUNCEMENT: str = "/{announcement_id}"
    DELETE_ANNOUNCEMENT: str = "/{announcement_id}"
    GET_ANNOUNCEMENTS: str = "/"


class AdminEndpoints:

    GET_ADMIN: str = "/{telegram_id}"
    ADD_ADMIN: str = "/{telegram_id}/add_admin"
    REMOVE_ADMIN: str = "/{telegram_id}/remove_admin"
    UPDATE_PERMISSIONS: str = "/{telegram_id}/update_permissions"
    BAN_USER: str = "/{telegram_id}/ban_user"
    UNBAN_USER: str = "/{telegram_id}/unban_user"
    ACCEPT_ANNOUNCEMENT: str = "/{announcement_id}/accept_announcement"
    DECLINE_ANNOUNCEMENT: str = "/{announcement_id}/decline_announcement"
    DELETE_ANNOUNCEMENT: str = "/{announcement_id}/delete_announcement"
    GET_USERS: str = "/users/"
    GET_BANNED_USERS: str = "/banned_users/"
    GET_ADMINS: str = "/admins/"


class DTOStub(BaseModel):
    # create and connect all dtos
    pass

class API:

    # TODO: Authorization
    __BASE_API_URL: str = settings.BASE_API_URL

    @classmethod
    async def _get_request(
            cls,
            endpoint: str,
            data: dict = {}
    ):
        pass

    @classmethod
    async def _post_request(
            cls,
            endpoint: str,
            data: dict = {}
    ):
        pass

    @classmethod
    async def _patch_request(
            cls,
            endpoint: str,
            data: dict = {}
    ):
        pass

    @classmethod
    async def _delete_request(
            cls,
            endpoint: str,
            data: dict = {}
    ):
        pass


class UserAPI(
    API,
    UserEndpoints
):

    __URL: str = "/user"

    @classmethod
    async def get_user(
            cls,
            telegram_id: int
    ) -> Union[DataStructure]:
        endpoint: str = cls.__URL + cls.GET_USER.format(
            telegram_id
        )

        return await cls._get_request(
            endpoint=endpoint
        )

    @classmethod
    async def create_user(
            cls,
            data: DTOStub
    ) -> Union[DataStructure]:
        endpoint: str = cls.__URL + cls.CREATE_USER

        return await cls._post_request(
            endpoint=endpoint,
            data=data.model_dump()
        )

    @classmethod
    async def update_user(
            cls,
            telegram_id: int,
            data: DTOStub
    ) -> Union[DataStructure]:
        endpoint: str = cls.__URL + cls.UPDATE_USER.format(
            telegram_id
        )

        return await cls._patch_request(
            endpoint=endpoint,
            data=data.model_dump()
        )

    @classmethod
    async def add_announcement(
            cls,
            telegram_id: int,
            data: DTOStub
    ) -> Union[DataStructure]:
        endpoint: str = cls.__URL + cls.ADD_ANNOUNCEMENT.format(
            telegram_id
        )

        return await cls._post_request(
            endpoint=endpoint,
            data=data.model_dump()
        )

    @classmethod
    #TODO: придумать решение для множественных параметров в get реквесте
    async def get_user_announcements(
            cls,
            telegram_id: int
    ) -> Union[DataStructure]:
        endpoint: str = cls.__URL + cls.GET_USER.format(
            telegram_id
        )

        return await cls._get_request(
            endpoint=endpoint
        )


class AnnouncementsAPI(
    API,
    AnnouncementEndpoints
):

    __URL: str = "/announcements"

    @classmethod
    async def get_announcement(
            cls,
            announcement_id: str
    ) -> Union[DataStructure]:
        endpoint: str = cls.__URL + cls.GET_ANNOUNCEMENT.format(
            announcement_id
        )

        return await cls._get_request(
            endpoint=endpoint
        )

    @classmethod
    async def delete_announcement(
            cls,
            announcement_id: str
    ) -> Union[DataStructure]:
        endpoint: str = cls.__URL + cls.DELETE_ANNOUNCEMENT.format(
            announcement_id
        )

        return await cls._get_request(
            endpoint=endpoint
        )

    @classmethod
    async def get_announcements(
            cls,
            data: DTOStub
    ) -> Union[DataStructure]:
        endpoint: str = cls.__URL + cls.GET_ANNOUNCEMENTS

        return await cls._get_request(
            endpoint=endpoint
        )


class AdminAPI(
    API,
    AdminEndpoints
):

    __URL: str = "/admin"

    @classmethod
    async def get_admin(
            cls,
            telegram_id: int
    ) -> Union[DataStructure]:
        endpoint: str = cls.__URL + cls.GET_ADMIN.format(
            telegram_id
        )

        return await cls._get_request(
            endpoint=endpoint
        )

    @classmethod
    async def get_admins(
            cls
    ) -> Union[DataStructure]:
        endpoint: str = cls.__URL + cls.GET_ADMINS

        return await cls._get_request(
            endpoint=endpoint
        )

    @classmethod
    async def get_users(
            cls
    ) -> Union[DataStructure]:
        endpoint: str = cls.__URL + cls.GET_USERS

        return await cls._get_request(
            endpoint=endpoint
        )

    @classmethod
    async def get_banned_users(
            cls
    ) -> Union[DataStructure]:
        endpoint: str = cls.__URL + cls.GET_BANNED_USERS.format

        return await cls._get_request(
            endpoint=endpoint
        )

    GET_ADMIN: str = "/{telegram_id}"
    ADD_ADMIN: str = "/{telegram_id}/add_admin"
    REMOVE_ADMIN: str = "/{telegram_id}/remove_admin"
    UPDATE_PERMISSIONS: str = "/{telegram_id}/update_permissions"
    BAN_USER: str = "/{telegram_id}/ban_user"
    UNBAN_USER: str = "/{telegram_id}/unban_user"
    ACCEPT_ANNOUNCEMENT: str = "/{announcement_id}/accept_announcement"
    DECLINE_ANNOUNCEMENT: str = "/{announcement_id}/decline_announcement"
    DELETE_ANNOUNCEMENT: str = "/{announcement_id}/delete_announcement"
    GET_USERS: str = "/users/"
    GET_BANNED_USERS: str = "/banned_users/"
    GET_ADMINS: str = "/admins/"

    @classmethod
    async def add_admin(
            cls,
            telegram_id: int,
            data: DTOStub
    ) -> Union[DataStructure]:
        endpoint: str = cls.__URL + cls.ADD_ADMIN.format(
            telegram_id
        )

        return await cls._post_request(
            endpoint=endpoint,
            data=data
        )

    @classmethod
    async def add_admin(
            cls,
            telegram_id: int,
            data: DTOStub
    ) -> Union[DataStructure]:
        endpoint: str = cls.__URL + cls.REMOVE_ADMIN.format(
            telegram_id
        )

        return await cls._delete_request(
            endpoint=endpoint,
            data=data
        )

    @classmethod
    async def update_permissions(
            cls,
            telegram_id: int,
            data: DTOStub
    ) -> Union[DataStructure]:
        endpoint: str = cls.__URL + cls.UPDATE_PERMISSIONS.format(
            telegram_id
        )

        return await cls._patch_request(
            endpoint=endpoint,
            data=data
        )

    @classmethod
    async def ban_user(
            cls,
            telegram_id: int,
            data: DTOStub
    ) -> Union[DataStructure]:
        endpoint: str = cls.__URL + cls.BAN_USER.format(
            telegram_id
        )

        return await cls._post_request(
            endpoint=endpoint,
            data=data
        )

    @classmethod
    async def unban_user(
            cls,
            telegram_id: int,
            data: DTOStub
    ) -> Union[DataStructure]:
        endpoint: str = cls.__URL + cls.UNBAN_USER.format(
            telegram_id
        )

        return await cls._post_request(
            endpoint=endpoint
        )

    @classmethod
    async def accept_announcement(
            cls,
            announcement_id: str
    ) -> Union[DataStructure]:
        endpoint: str = cls.__URL + cls.ACCEPT_ANNOUNCEMENT.format(
            announcement_id
        )

        return await cls._patch_request(
            endpoint=endpoint
        )

    @classmethod
    async def decline_announcement(
            cls,
            announcement_id: str
    ) -> Union[DataStructure]:
        endpoint: str = cls.__URL + cls.DECLINE_ANNOUNCEMENT.format(
            announcement_id
        )

        return await cls._patch_request(
            endpoint=endpoint
        )

    @classmethod
    async def delete_announcement(
            cls,
            announcement_id: str
    ) -> Union[DataStructure]:
        endpoint: str = cls.__URL + cls.DELETE_ANNOUNCEMENT.format(
            announcement_id
        )

        return await cls._delete_request(
            endpoint=endpoint
        )


class OpenStreetMapAPI:

    __URL = "https://nominatim.openstreetmap.org/reverse"

    # @classmethod
    # async def get_address(cls, latitude: float, longitude: float) -> 'DataStructure':
    #     url: str = cls.__URL
    #
    #     data: dict = {
    #         "format": "json",
    #         "lat": latitude,
    #         "lon": longitude
    #     }
    #
    #     return await GetRequest(url=url,
    #                             data=data).send_request()
    #
    # @classmethod
    # async def get_location(cls, name: str) -> 'DataStructure':
    #     url: str = "https://nominatim.openstreetmap.org/search.php"
    #
    #     data: dict = {
    #         "format": "json",
    #         "city": name,
    #         "country": "Ukraine"
    #     }
    #
    #     response = requests.get(url, params=data).json()
    #     if response:
    #         response_data: dict = {
    #             "latitude": float(response[0]['lat']),
    #             "longitude": float(response[0]['lon']),
    #         }
    #
    #         return response_data
    #     return None