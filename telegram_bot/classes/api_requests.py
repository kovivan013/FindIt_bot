import aiohttp

from network.endpoints import (
    UserEndpoints,
    AnnouncementEndpoints,
    AdminEndpoints
)
from utils import utils
from pydantic import BaseModel
from typing import Union
from network.request_classes import (
    GetRequest,
    PostRequest,
    PatchRequest,
    PutRequest,
    DeleteRequest
)
from common.interfaces import DataStructure
from common.classes import AnnouncementSort
from common import dtos
from config import settings


class API:

    __BASE_API_URL: str = settings.BASE_API_URL

    @classmethod
    async def _get_request(
            cls,
            auth: int,
            *,
            endpoint: str,
            data: dict = {}
    ):
        url: str = cls.__BASE_API_URL + endpoint
        return await GetRequest(
            url=url,
            data=data
        ).send_request(auth)

    @classmethod
    async def _post_request(
            cls,
            auth: int,
            *,
            endpoint: str,
            data: dict = {}
    ):
        url: str = cls.__BASE_API_URL + endpoint
        return await PostRequest(
            url=url,
            data=data
        ).send_request(auth)

    @classmethod
    async def _patch_request(
            cls,
            auth: int,
            *,
            endpoint: str,
            data: dict = {}
    ):
        url: str = cls.__BASE_API_URL + endpoint
        return await PatchRequest(
            url=url,
            data=data
        ).send_request(auth)

    @classmethod
    async def _put_request(
            cls,
            auth: int,
            *,
            endpoint: str,
            data: dict = {}
    ):
        url: str = cls.__BASE_API_URL + endpoint
        return await PutRequest(
            url=url,
            data=data
        ).send_request(auth)

    @classmethod
    async def _delete_request(
            cls,
            auth: int,
            *,
            endpoint: str,
            data: dict = {}
    ):
        url: str = cls.__BASE_API_URL + endpoint
        return await DeleteRequest(
            url=url,
            data=data
        ).send_request(auth)


class UserAPI(
    API,
    UserEndpoints
):

    __URL: str = "/user"

    @classmethod
    async def get_user(
            cls,
            auth: int,
            *,
            telegram_id: int
    ) -> Union[DataStructure]:
        endpoint: str = cls.__URL + cls.GET_USER.format(
            telegram_id
        )

        return await cls._get_request(
            auth,
            endpoint=endpoint
        )

    @classmethod
    async def create_user(
            cls,
            auth: int,
            *,
            data: dtos.CreateUserDTO
    ) -> Union[DataStructure]:
        endpoint: str = cls.__URL + cls.CREATE_USER

        return await cls._post_request(
            auth,
            endpoint=endpoint,
            data=data.model_dump()
        )

    @classmethod
    async def update_user(
            cls,
            auth: int,
            *,
            telegram_id: int,
            data: dtos.UpdateUserDTO
    ) -> Union[DataStructure]:
        endpoint: str = cls.__URL + cls.UPDATE_USER.format(
            telegram_id
        )

        return await cls._patch_request(
            auth,
            endpoint=endpoint,
            data=data.model_dump()
        )

    @classmethod
    async def add_announcement(
            cls,
            auth: int,
            *,
            telegram_id: int,
            data: dtos.AddAnnouncementDTO
    ) -> Union[DataStructure]:
        endpoint: str = cls.__URL + cls.ADD_ANNOUNCEMENT.format(
            telegram_id
        )

        return await cls._post_request(
            auth,
            endpoint=endpoint,
            data=data.model_dump()
        )

    @classmethod
    async def get_user_announcements(
            cls,
            auth: int,
            *,
            telegram_id: int,
            mode: int = 0,
            status: int = 0,
            limit: int = 1,
            page: int = 0
    ) -> Union[DataStructure]:
        endpoint: str = cls.__URL + cls.GET_USER_ANNOUNCEMENTS.format(
            telegram_id
        )
        data = dtos.GetUserAnnouncementsDTO().model_validate(
            locals()
        )

        return await cls._get_request(
            auth,
            endpoint=endpoint,
            data=data.model_dump()
        )


class AnnouncementsAPI(
    API,
    AnnouncementEndpoints
):

    __URL: str = "/announcements"

    @classmethod
    async def get_announcement(
            cls,
            auth: int,
            *,
            announcement_id: str
    ) -> Union[DataStructure]:
        endpoint: str = cls.__URL + cls.GET_ANNOUNCEMENT.format(
            announcement_id
        )

        return await cls._get_request(
            auth,
            endpoint=endpoint
        )

    @classmethod
    async def delete_announcement(
            cls,
            auth: int,
            *,
            announcement_id: str
    ) -> Union[DataStructure]:
        endpoint: str = cls.__URL + cls.DELETE_ANNOUNCEMENT.format(
            announcement_id
        )

        return await cls._get_request(
            auth,
            endpoint=endpoint
        )

    @classmethod
    async def get_announcements(
            cls,
            auth: int,
            query: str,
            location: str = "",
            mode: int = 0,
            status: int = 0,
            limit: int = 1,
            page: int = 0,
            start_from: str = AnnouncementSort.latest
    ) -> Union[DataStructure]:
        endpoint: str = cls.__URL + cls.GET_ANNOUNCEMENTS
        data = dtos.GetAnnouncementsDTO().model_validate(
            locals()
        )

        return await cls._get_request(
            auth,
            endpoint=endpoint,
            data=data.model_dump()
        )


class AdminAPI(
    API,
    AdminEndpoints
):

    __URL: str = "/admin"

    @classmethod
    async def get_admin(
            cls,
            auth: int,
            *,
            telegram_id: int
    ) -> Union[DataStructure]:
        endpoint: str = cls.__URL + cls.GET_ADMIN.format(
            telegram_id
        )

        return await cls._get_request(
            auth,
            endpoint=endpoint
        )

    @classmethod
    async def get_admins(
            cls,
            auth: int,
            limit: int = 1,
            page: int = 0
    ) -> Union[DataStructure]:
        endpoint: str = cls.__URL + cls.GET_ADMINS
        data = dtos.GetAdminsDTO().model_validate(
            locals()
        )

        return await cls._get_request(
            auth,
            endpoint=endpoint,
            data=data.model_dump()
        )

    @classmethod
    async def get_users(
            cls,
            auth: int,
            limit: int = 1,
            page: int = 0
    ) -> Union[DataStructure]:
        endpoint: str = cls.__URL + cls.GET_USERS
        data = dtos.GetUsersDTO().model_validate(
            locals()
        )

        return await cls._get_request(
            auth,
            endpoint=endpoint,
            data=data.model_dump()
        )

    @classmethod
    async def get_banned_users(
            cls,
            auth: int,
            limit: int = 1,
            page: int = 0
    ) -> Union[DataStructure]:
        endpoint: str = cls.__URL + cls.GET_BANNED_USERS.format
        data = dtos.GetBannedUsersDTO().model_validate(
            locals()
        )

        return await cls._get_request(
            auth,
            endpoint=endpoint,
            data=data.model_dump()
        )

    @classmethod
    async def add_admin(
            cls,
            auth: int,
            *,
            telegram_id: int,
            data: dtos.AddAdminDTO
    ) -> Union[DataStructure]:
        endpoint: str = cls.__URL + cls.ADD_ADMIN.format(
            telegram_id
        )

        return await cls._post_request(
            auth,
            endpoint=endpoint,
            data=data.model_dump()
        )

    @classmethod
    async def remove_admin(
            cls,
            auth: int,
            *,
            telegram_id: int
    ) -> Union[DataStructure]:
        endpoint: str = cls.__URL + cls.REMOVE_ADMIN.format(
            telegram_id
        )

        return await cls._delete_request(
            auth,
            endpoint=endpoint
        )

    @classmethod
    async def update_permissions(
            cls,
            auth: int,
            *,
            telegram_id: int,
            data: dtos.UpdatePermissionsDTO
    ) -> Union[DataStructure]:
        endpoint: str = cls.__URL + cls.UPDATE_PERMISSIONS.format(
            telegram_id
        )

        return await cls._patch_request(
            auth,
            endpoint=endpoint,
            data=data.model_dump()
        )

    @classmethod
    async def ban_user(
            cls,
            auth: int,
            *,
            telegram_id: int,
            data: dtos.BanUserDTO
    ) -> Union[DataStructure]:
        endpoint: str = cls.__URL + cls.BAN_USER.format(
            telegram_id
        )

        return await cls._post_request(
            auth,
            endpoint=endpoint,
            data=data.model_dump()
        )

    @classmethod
    async def unban_user(
            cls,
            auth: int,
            *,
            telegram_id: int
    ) -> Union[DataStructure]:
        endpoint: str = cls.__URL + cls.UNBAN_USER.format(
            telegram_id
        )

        return await cls._post_request(
            auth,
            endpoint=endpoint
        )

    @classmethod
    async def accept_announcement(
            cls,
            auth: int,
            *,
            announcement_id: str
    ) -> Union[DataStructure]:
        endpoint: str = cls.__URL + cls.ACCEPT_ANNOUNCEMENT.format(
            announcement_id
        )

        return await cls._patch_request(
            auth,
            endpoint=endpoint
        )

    @classmethod
    async def decline_announcement(
            cls,
            auth: int,
            *,
            announcement_id: str
    ) -> Union[DataStructure]:
        endpoint: str = cls.__URL + cls.DECLINE_ANNOUNCEMENT.format(
            announcement_id
        )

        return await cls._patch_request(
            auth,
            endpoint=endpoint
        )

    @classmethod
    async def delete_announcement(
            cls,
            auth: int,
            *,
            announcement_id: str
    ) -> Union[DataStructure]:
        endpoint: str = cls.__URL + cls.DELETE_ANNOUNCEMENT.format(
            announcement_id
        )

        return await cls._delete_request(
            auth,
            endpoint=endpoint
        )


class OpenStreetMapAPI(API):

    @classmethod
    async def get_address(
            cls,
            latitude: float,
            longitude: float
    ) -> Union[DataStructure]:
        url: str = "https://nominatim.openstreetmap.org/reverse"
        params: dict = {
            "format": "json",
            "lat": latitude,
            "lon": longitude
        }

        async with aiohttp.ClientSession() as session:
            return await (
                await session.get(
                    url=url,
                    params=params
                )
            ).json()

    @classmethod
    async def get_location(
            cls,
            name: str
    ) -> Union[DataStructure]:
        url: str = "https://nominatim.openstreetmap.org/search.php"
        params: dict = {
            "format": "json",
            "city": name,
            "country": "Ukraine"
        }

        async with aiohttp.ClientSession() as session:
            response = await (
                await session.get(
                    url=url,
                    params=params
                )
            ).json()

        if response:
            return {
                "latitude": float(response[0]['lat']),
                "longitude": float(response[0]['lon']),
            }

        return {}

import asyncio

print(asyncio.run(AnnouncementsAPI.get_announcements(auth=123, query="tesdsrfghds", limit=10, page=3)))

