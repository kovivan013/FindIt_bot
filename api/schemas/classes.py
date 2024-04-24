from enum import Enum
from pydantic import BaseModel, Field


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


class AdminPermissions:

    SUPER_ADMIN: bool = False
    MANAGE_PERMISSIONS: bool = False
    MANAGE_ANNOUNCEMENTS: bool = False
    DELETE_ANNOUNCEMENTS: bool = False
    MANAGE_USERS: bool = False

    def __getattribute__(self, item):
        return item


class AnnouncementStatus:

    ACTIVE: int = 0
    COMPLETED: int = 1
    PENDING: int = 2


class UserStatus:

    ACTIVE: int = 0
    BANNED: int = 1


class UserMode:

    FINDER: int = 0
    DETECTIVE: int = 1


class AnnouncementSort(Enum):

    oldest: str = "oldest"
    latest: str = "latest"

    @property
    def _value(self):
        return self.value

    @_value.getter
    def _value(self):
        return self.value == self.latest.value


ADMIN_PERMISSIONS = AdminPermissions()





