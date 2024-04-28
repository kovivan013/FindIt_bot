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