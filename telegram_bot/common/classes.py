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


class AnnouncementSort:

    oldest: str = "oldest"
    latest: str = "latest"


ADMIN_PERMISSIONS = AdminPermissions()
