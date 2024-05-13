from string import ascii_letters, digits

class AdminPermissions:

    SUPER_ADMIN: bool = False
    MANAGE_PERMISSIONS: bool = False
    MANAGE_ANNOUNCEMENTS: bool = False
    DELETE_ANNOUNCEMENTS: bool = False
    MANAGE_USERS: bool = False

    def __getattribute__(self, item):
        return item


class ServicePhotos:

    LOGO: str = "logo.png"
    AVATAR: str = "avatar.png"
    ALLOW_ACCESS: str = "allow_access.png"
    CONTACT: str = "contact.png"
    DATE: str = "date.png"
    DECLINE_ACCESS: str = "decline_access.png"
    DESCRIPTION: str = "description.png"
    FILTERS: str = " filters.png"
    FINISH: str = "finish.png"
    ANNOUNCEMENTS_DASHBOARD: str = "announcements_dashboard.png"
    ANNOUNCEMENTS_LIST: str = "announcements_list.png"
    LOCATION: str = "location.png"
    NAME: str = "name.png"
    NOTIFICATIONS: str = "notifications.png"
    PHOTO: str = "photo.png"
    TAGS: str = "tags.png"
    TIME: str = "time.png"
    USERNAME: str = "username.png"
    USER_ANNOUNCEMENTS: str ="user_announcements.png"
    IS_YOUR_THING: str = "is_your_thing.png"
    UNKNOWN_ANNOUNCEMENT: str = "unknown_announcement.png"


class Symbols:

    UKRAINIAN_ALPHABET: str = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюяАБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ"
    ENGLISH_ALPHABET: str = ascii_letters
    DIGITS: str = digits


class FSMActions:

    APP_CONFIG: str = "/app_config"
    CREATE_USER: str = "/create_user"
    UPDATE_USER: str = "/update_user"
    ADD_ANNOUNCEMENT: str = "/add_announcement"
    GET_USER_ANNOUNCEMENTS: str = "/get_user_announcements"
    GET_ANNOUNCEMENTS: str = "/get_announcements"
    ADD_ADMIN: str = "/add_admin"
    UPDATE_PERMISSIONS: str = "/update_permissions"
    BAN_USER: str = "/ban_user"
    GET_USERS: str = "/get_users"
    GET_BANNED_USERS: str = "/get_banned_users"
    GET_ADMINS: str = "/get_admins"


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


class AnnouncementSort:

    oldest: str = "oldest"
    latest: str = "latest"


ADMIN_PERMISSIONS = AdminPermissions()
