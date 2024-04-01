class Endpoints:

    GET_USER: str = "/{telegram_id}"
    CREATE_USER: str = "/create_user"
    UPDATE_USER: str = "/{telegram_id}"
    GET_ANNOUNCEMENT: str = "/{announcement_id}"
    ADD_ANNOUNCEMENT: str = "/{telegram_id}/add_announcement"
    DELETE_ANNOUNCEMENT: str = "/{announcement_id}"
    GET_ANNOUNCEMENTS: str = "/"
    GET_USER_ANNOUNCEMENTS: str = "/announcements"


class Status:

    ACTIVE: int = 0
    COMPLETED: int = 1
    PENDING: int = 2



