class UserEndpoints:

    GET_USER: str = "/{}"
    CREATE_USER: str = "/create_user"
    UPDATE_USER: str = "/{}"
    ADD_ANNOUNCEMENT: str = "/{}/add_announcement"
    GET_USER_ANNOUNCEMENTS: str = "/{}/announcements"
    SEND_NOTIFICATION: str = "/{}/send_notification"


class AnnouncementEndpoints:

    GET_ANNOUNCEMENT: str = "/{}"
    DELETE_ANNOUNCEMENT: str = "/{}"
    GET_ANNOUNCEMENTS: str = "/"


class AdminEndpoints:

    GET_ADMIN: str = "/{}"
    ADD_ADMIN: str = "/{}/add_admin"
    REMOVE_ADMIN: str = "/{}/remove_admin"
    UPDATE_PERMISSIONS: str = "/{}/update_permissions"
    BAN_USER: str = "/{}/ban_user"
    UNBAN_USER: str = "/{}/unban_user"
    ACCEPT_ANNOUNCEMENT: str = "/{}/accept_announcement"
    DECLINE_ANNOUNCEMENT: str = "/{}/decline_announcement"
    DELETE_ANNOUNCEMENT: str = "/{}/delete_announcement"
    GET_USERS: str = "/users/"
    GET_BANNED_USERS: str = "/banned_users/"
    GET_ADMINS: str = "/admins/"