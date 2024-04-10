from enum import Enum

class Endpoints:

    GET_USER: str = "/{telegram_id}"
    CREATE_USER: str = "/create_user"
    UPDATE_USER: str = "/{telegram_id}"
    GET_ANNOUNCEMENT: str = "/{announcement_id}"
    ADD_ANNOUNCEMENT: str = "/{telegram_id}/add_announcement"
    DELETE_ANNOUNCEMENT: str = "/{announcement_id}"
    GET_ANNOUNCEMENTS: str = "/"
    GET_USER_ANNOUNCEMENTS: str = "/{telegram_id}/announcements"
    ADD_ADMIN: str = "/{telegram_id}/add_admin"
    BAN_USER: str = "/{telegram_id}/ban_user"
    ACCEPT_ANNOUNCEMENT: str = "/{announcement_id}/accept_announcement"
    DECLINE_ANNOUNCEMENT: str = "/{announcement_id}/decline_announcement"


class UserEndpoints:

    GET_USER: str = "/{telegram_id}"
    CREATE_USER: str = "/create_user"
    UPDATE_USER: str = "/{telegram_id}"
    ADD_ANNOUNCEMENT: str = "/{telegram_id}/add_announcement"
    GET_USER_ANNOUNCEMENTS: str = "/{telegram_id}/announcements"


class AnnouncementEndpoints:

    GET_ANNOUNCEMENT: str = "/{announcement_id}"
    DELETE_ANNOUNCEMENT: str = "/{announcement_id}"
    GET_ANNOUNCEMENTS: str = "/"


class AdminEndpoints:

    ADD_ADMIN: str = "/{telegram_id}/add_admin"
    BAN_USER: str = "/{telegram_id}/ban_user"
    ACCEPT_ANNOUNCEMENT: str = "/{announcement_id}/accept_announcement"
    DECLINE_ANNOUNCEMENT: str = "/{announcement_id}/decline_announcement"
    DELETE_ANNOUNCEMENT: str = "/{announcement_id}/delete_announcement"


class AdminPermissions:

    MANAGE_ANNOUNCEMENTS: bool = False
    BAN_USERS: bool = False
    DELETE_ANNOUNCEMENTS: bool = False
    ADD_ADMINS: bool = False

class AnnouncementStatus:

    ACTIVE: int = 0
    COMPLETED: int = 1
    PENDING: int = 2


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





