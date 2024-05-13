from . import debug
from config import dp

from .admin import (
    admin_panel,
    stats,
    users,
    announcements,
    placement_requests,
    support_requests
)

from .user import (
    signup,
    info_about,
    dashboard,
    marketplace,
    user_announcements,
    notifications,
    support
)


def register_events():
    signup.register(dp)
    dashboard.register(dp)
    debug.register(dp)
