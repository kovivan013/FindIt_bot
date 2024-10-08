from fastapi import (
    APIRouter,
    Depends,
    Response,
    Request,
    Query,
)
from typing_extensions import Annotated
from datetime import datetime
from typing import Union, AsyncIterable, Dict, Any
from starlette import status as HTTPStatus
from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from database.core import (
    core
)
from database.models.models import (
    Users,
    Admins,
    Announcements,
    BannedUsers
)
from common.dto.user import (
    UserCreate,
    UserUpdate
)
from common.dto.admin import (
    AdminAdd,
    PermissionsUpdate,
    UserBan
)
from common.dto.announcement import (
    AddAnnouncement
)
from schemas.schemas import (
    BaseUser,
    BaseAdmin,
    BaseAnnouncement,
    UserAnnouncementsResponse,
    AdminPermissions,
    BannedUser
)
from schemas.classes import (
    AdminEndpoints,
    AnnouncementStatus,
    AnnouncementSort,
    UserMode,
    UserStatus,
    ADMIN_PERMISSIONS
)
from config import settings
from services import exceptions
from services.errors_reporter import Reporter
from schemas.base import DataStructure
from utils import utils
from utils.utils import OAuth2


admin_router = APIRouter()


@admin_router.get(AdminEndpoints.GET_ADMIN)
async def get_admin(
        telegram_id: int,
        request: Request,
        session: AsyncSession = Depends(
            core.create_sa_session
        )
) -> Union[DataStructure]:
    await OAuth2._check_token(
        request,
        session,
        require_admin=True
    )

    result = DataStructure()
    admin = await session.get(
        Admins,
        telegram_id
    )

    if not admin:
        return await Reporter(
            exception=exceptions.ItemNotFound,
            message="Admin not found"
        )._report()

    await session.close()

    result.data = admin.as_model().model_dump()
    result._status = HTTPStatus.HTTP_200_OK

    return result


@admin_router.get(AdminEndpoints.GET_ADMINS)
async def get_admins(
        request: Request,
        limit: int = Query(
            1,
            gt=0
        ),
        page: int = Query(
            0,
            gt=-1
        ),
        session: AsyncSession = Depends(
            core.create_sa_session
        )
) -> Union[DataStructure]:
    await OAuth2._check_token(
        request,
        session,
        require_admin=True
    )
    result = DataStructure()

    query_result = await session.execute(
        select(
            Admins
        ).order_by(
            Admins.added_at.desc()
        )
    )
    admins: dict = {}
    offset: int = page * limit

    for i, admin in enumerate(query_result.scalars().all()):
        if i in range(
            offset,
            offset + limit
        ):
            admins.update(
                {
                    admin.telegram_id: admin.as_dict()
                }
            )

    await session.close()

    result.data = admins
    result._status = HTTPStatus.HTTP_200_OK

    return result


@admin_router.get(AdminEndpoints.GET_USERS)
async def get_users(
        request: Request,
        limit: int = Query(
            1,
            gt=0
        ),
        page: int = Query(
            0,
            gt=-1
        ),
        session: AsyncSession = Depends(
            core.create_sa_session
        )
) -> Union[DataStructure]:
    await OAuth2._check_token(
        request,
        session,
        require_admin=True
    )
    result = DataStructure()

    query_result = await session.execute(
        select(
            Users
        ).order_by(
            Users.created_at.desc()
        )
    )
    users: dict = {}
    offset: int = page * limit

    for i, user in enumerate(query_result.scalars().all()):
        if i in range(
            offset,
            offset + limit
        ):
            users.update(
                {
                    user.telegram_id: user.as_dict()
                }
            )

    await session.close()

    result.data = users
    result._status = HTTPStatus.HTTP_200_OK

    return result


@admin_router.get(AdminEndpoints.GET_BANNED_USERS)
async def get_banned_users(
        request: Request,
        limit: int = Query(
            1,
            gt=0
        ),
        page: int = Query(
            0,
            gt=-1
        ),
        session: AsyncSession = Depends(
            core.create_sa_session
        )
) -> Union[DataStructure]:
    await OAuth2._check_token(
        request,
        session,
        require_admin=True
    )
    result = DataStructure()

    query_result = await session.execute(
        select(
            BannedUsers
        ).order_by(
            BannedUsers.banned_at.desc()
        )
    )
    banned_users: dict = {}
    offset: int = page * limit

    for i, banned_user in enumerate(query_result.scalars().all()):
        if i in range(
            offset,
            offset + limit
        ):
            banned_users.update(
                {
                    banned_user.telegram_id: banned_user.as_dict()
                }
            )

    await session.close()

    result.data = banned_users
    result._status = HTTPStatus.HTTP_200_OK

    return result


@admin_router.post(AdminEndpoints.ADD_ADMIN)
async def add_admin(
        telegram_id: int,
        parameters: AdminAdd,
        request: Request,
        session: AsyncSession = Depends(
            core.create_sa_session
        )
) -> Union[DataStructure]:
    await OAuth2._check_token(
        request,
        session,
        admin_permissions=[
            ADMIN_PERMISSIONS.SUPER_ADMIN
        ]
    )

    result = DataStructure()
    banned_user = await session.get(
        BannedUsers,
        telegram_id
    )

    if banned_user:
        return await Reporter(
            exception=exceptions.NoAccess,
            message="You cannot grant admin permissions user that banned"
        )._report()

    user = await session.get(
        Users,
        telegram_id
    )

    if not user:
        return await Reporter(
            exception=exceptions.ItemNotFound,
            message="User not found"
        )._report()

    new_admin = await session.get(
        Admins,
        telegram_id
    )

    if new_admin:
        return await Reporter(
            exception=exceptions.ItemExists,
            message="Admin already exists"
        )._report()

    new_admin_permissions = AdminPermissions().model_validate(
        parameters.permissions
    ).model_dump(
        exclude_defaults=True
    )

    verify_permissions = await OAuth2._check_new_admin_permissions(
        permissions=new_admin_permissions.keys(),
        request=request,
        session=session
    )
    if not verify_permissions.success:
        return verify_permissions

    data_scheme = BaseAdmin(
        telegram_id=telegram_id,
        permissions=new_admin_permissions,
        added_at=utils.timestamp()
    )

    session.add(
        Admins(
            **data_scheme.model_dump()
        )
    )

    await session.commit()
    await session.close()

    result.data = data_scheme.model_dump()
    result._status = HTTPStatus.HTTP_201_CREATED

    return result


@admin_router.delete(AdminEndpoints.REMOVE_ADMIN)
async def remove_admin(
        telegram_id: int,
        request: Request,
        session: AsyncSession = Depends(
            core.create_sa_session
        )
) -> Union[DataStructure]:
    token = await OAuth2._check_token(
        request,
        session,
        admin_permissions=[
            ADMIN_PERMISSIONS.SUPER_ADMIN
        ]
    )
    result = DataStructure()

    if token.id_ == telegram_id:
        return await Reporter(
            exception=exceptions.NoAccess,
            message="You cannot delete your own admin profile"
        )._report()

    admin = await session.get(
        Admins,
        telegram_id
    )

    if not admin:
        return await Reporter(
            exception=exceptions.ItemNotFound,
            message="Admin not found"
        )._report()

    if ADMIN_PERMISSIONS.SUPER_ADMIN in admin.permissions:
        if token.id_ not in settings.OWNERS:
            return await Reporter(
                exception=exceptions.NoAccess,
                message="Not enought permissions"
            )._report()

    await session.delete(
        admin
    )
    await session.commit()
    await session.close()

    result._status = HTTPStatus.HTTP_200_OK

    return result


@admin_router.patch(AdminEndpoints.UPDATE_PERMISSIONS)
async def update_permissions(
        telegram_id: int,
        parameters: PermissionsUpdate,
        request: Request,
        session: AsyncSession = Depends(
            core.create_sa_session
        )
) -> Union[DataStructure]:
    token = await OAuth2._check_token(
        request,
        session,
        admin_permissions=[
            ADMIN_PERMISSIONS.SUPER_ADMIN
        ]
    )
    result = DataStructure()

    if token.id_ == telegram_id:
        return await Reporter(
            exception=exceptions.NoAccess,
            message="You cannot manage your own permissions"
        )._report()

    admin = await session.get(
        Admins,
        telegram_id
    )
    permissions = AdminPermissions().model_validate(
        parameters.permissions
    ).model_dump(
        exclude_defaults=True
    )

    if not admin:
        return await Reporter(
            exception=exceptions.ItemNotFound,
            message="Admin not found"
        )._report()

    if ADMIN_PERMISSIONS.SUPER_ADMIN not in admin.permissions:
        if ADMIN_PERMISSIONS.SUPER_ADMIN in permissions and permissions[
            ADMIN_PERMISSIONS.SUPER_ADMIN
        ]:
            if token.id_ not in settings.OWNERS:
                return await Reporter(
                    exception=exceptions.NoAccess,
                    message="Not enought permissions"
                )._report()

    admin.permissions = permissions

    await session.commit()
    await session.close()

    result.data = permissions
    result._status = HTTPStatus.HTTP_200_OK

    return result


@admin_router.post(AdminEndpoints.BAN_USER)
async def ban_user(
        telegram_id: int,
        parameters: UserBan,
        request: Request,
        session: AsyncSession = Depends(
            core.create_sa_session
        )
) -> Union[DataStructure]:
    token = await OAuth2._check_token(
        request,
        session,
        admin_permissions=[
            ADMIN_PERMISSIONS.MANAGE_USERS
        ]
    )
    result = DataStructure()

    if token.id_ == telegram_id:
        return await Reporter(
            exception=exceptions.NoAccess,
            message="You cannot ban your own account"
        )._report()

    if parameters.duration < 60:
        return await Reporter(
            exception=exceptions.NoAccess,
            message="Duration must be > than 60 seconds"
        )._report()

    banned_user = await session.get(
        BannedUsers,
        telegram_id
    )

    if banned_user:
        return await Reporter(
            exception=exceptions.NoAccess,
            message="The user has already banned"
        )._report()

    user = await session.get(
        Users,
        telegram_id
    )

    if not user:
        return await Reporter(
            exception=exceptions.ItemNotFound,
            message="User not found"
        )._report()

    admin = await session.get(
        Admins,
        telegram_id
    )

    if admin:
        if token.id_ not in settings.OWNERS:
            requester = await session.get(
                Admins,
                token.id_
            )

            if ADMIN_PERMISSIONS.SUPER_ADMIN in admin.permissions or ADMIN_PERMISSIONS.SUPER_ADMIN not in requester.permissions:
                return await Reporter(
                    exception=exceptions.NoAccess,
                    message="Not enought permissions"
                )._report()

        await session.delete(
            admin
        )

    data_scheme = BannedUser().model_validate(
        parameters.model_dump()
    )
    data_scheme.telegram_id = telegram_id
    data_scheme.administrator = token.id_
    data_scheme.banned_at = utils.timestamp()
    data_scheme.until = utils.timestamp() + parameters.duration

    session.add(
        BannedUsers(
            **data_scheme.model_dump()
        )
    )

    await session.commit()
    await session.close()

    result.data = data_scheme.model_dump()
    result._status = HTTPStatus.HTTP_200_OK

    return result


@admin_router.post(AdminEndpoints.UNBAN_USER)
async def unban_user(
        telegram_id: int,
        request: Request,
        session: AsyncSession = Depends(
            core.create_sa_session
        )
) -> Union[DataStructure]:
    token = await OAuth2._check_token(
        request,
        session,
        admin_permissions=[
            ADMIN_PERMISSIONS.MANAGE_USERS
        ]
    )
    result = DataStructure()

    if token.id_ == telegram_id:
        return await Reporter(
            exception=exceptions.NoAccess,
            message="You cannot unban your own account"
        )._report()

    banned_user = await session.get(
        BannedUsers,
        telegram_id
    )

    if not banned_user:
        return await Reporter(
            exception=exceptions.ItemNotFound,
            message="User not banned"
        )

    await session.delete(
        banned_user
    )
    await session.commit()
    await session.close()

    result._status = HTTPStatus.HTTP_200_OK

    return result


@admin_router.patch(AdminEndpoints.ACCEPT_ANNOUNCEMENT)
async def accept_announcement(
        announcement_id: str,
        request: Request,
        session: AsyncSession = Depends(
            core.create_sa_session
        )
) -> Union[DataStructure]:
    token = await OAuth2._check_token(
        request,
        session,
        admin_permissions=[
            ADMIN_PERMISSIONS.MANAGE_ANNOUNCEMENTS
        ]
    )
    result = DataStructure()

    announcement = await session.get(
        Announcements,
        announcement_id
    )

    if not announcement:
        return await Reporter(
            exception=exceptions.ItemNotFound,
            message="The announcement not found"
        )._report()

    if announcement.owner_id == token.id_:
        return await Reporter(
            exception=exceptions.NoAccess,
            message="You cannot accept the placement of your own announcement"
        )._report()

    if announcement.status != AnnouncementStatus.PENDING:
        return await Reporter(
            exception=exceptions.NoAccess,
            message="The announcement was processed by another administrator"
        )._report()

    banned_user = await session.get(
        BannedUsers,
        announcement.owner_id
    )

    if banned_user:
        return await Reporter(
            exception=exceptions.NoAccess,
            message="The owner of the announcement is banned, so you cannot accept the announcement placement"
        )._report()

    announcement.status = AnnouncementStatus.ACTIVE

    await session.commit()
    await session.close()

    result.message = "The announcement has been successfully placed."
    result._status = HTTPStatus.HTTP_200_OK

    return result


@admin_router.patch(AdminEndpoints.DECLINE_ANNOUNCEMENT)
async def decline_announcement(
        announcement_id: str,
        request: Request,
        session: AsyncSession = Depends(
            core.create_sa_session
        )
) -> Union[DataStructure]:
    token = await OAuth2._check_token(
        request,
        session,
        admin_permissions=[
            ADMIN_PERMISSIONS.MANAGE_ANNOUNCEMENTS
        ]
    )
    result = DataStructure()

    announcement = await session.get(
        Announcements,
        announcement_id
    )

    if not announcement:
        return await Reporter(
            exception=exceptions.ItemNotFound,
            message="The announcement not found"
        )._report()

    if announcement.owner_id == token.id_:
        return await Reporter(
            exception=exceptions.NoAccess,
            message="You cannot decline the placement of your own announcement"
        )._report()

    if announcement.status != AnnouncementStatus.PENDING:
        return await Reporter(
            exception=exceptions.NoAccess,
            message="The announcement was processed by another administrator"
        )._report()

    await session.delete(
        announcement
    )

    await session.commit()
    await session.close()

    result.message = "The announcement placement successfully declined."
    result._status = HTTPStatus.HTTP_200_OK

    return result


@admin_router.delete(AdminEndpoints.DELETE_ANNOUNCEMENT)
async def delete_announcement(
        announcement_id: str,
        request: Request,
        session: AsyncSession = Depends(
            core.create_sa_session
        )
) -> Union[DataStructure]:
    await OAuth2._check_token(
        request,
        session,
        admin_permissions=[
            ADMIN_PERMISSIONS.DELETE_ANNOUNCEMENTS
        ]
    )
    result = DataStructure()

    announcement = await session.get(
        Announcements,
        announcement_id
    )

    if not announcement:
        return await Reporter(
            exception=exceptions.ItemNotFound,
            message="The announcement not found"
        )._report()

    if announcement.status != AnnouncementStatus.ACTIVE:
        return await Reporter(
            exception=exceptions.NoAccess,
            message="The announcement doesn`t have an active status, so it cannot be deleted"
        )

    await session.delete(
        announcement
    )

    await session.commit()
    await session.close()

    result.message = "The announcement has been successfully deleted"
    result._status = HTTPStatus.HTTP_200_OK

    return result

