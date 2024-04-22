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
    Announcements
)
from common.dto.user import (
    UserCreate,
    UserUpdate
)
from common.dto.admin import (
    AdminAdd
)
from common.dto.announcement import (
    AddAnnouncement
)
from schemas.schemas import (
    BaseUser,
    BaseAdmin,
    BaseAnnouncement,
    UserAnnouncementsResponse,
    AdminPermissions
)
from schemas.classes import (
    AdminEndpoints,
    AnnouncementStatus,
    AnnouncementSort,
    UserMode,
    ADMIN_PERMISSIONS
)
from config import settings
from services import exceptions
from services.errors_reporter import Reporter
from schemas.base import DataStructure
from utils import utils
from utils.utils import OAuth2


admin_router = APIRouter()

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
        permissions=new_admin_permissions
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

@admin_router.post(AdminEndpoints.REMOVE_ADMIN)
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

@admin_router.post(AdminEndpoints.BAN_USER)
async def ban_user(
        telegram_id: int,
        request: Request,
        session: AsyncSession = Depends(
            core.create_sa_session
        )
) -> Union[DataStructure]:
    await OAuth2._check_token(
        request,
        session,
        admin_permissions=[
            ADMIN_PERMISSIONS.BAN_USERS
        ]
    )
    result = DataStructure()

    return result

@admin_router.post(AdminEndpoints.ACCEPT_ANNOUNCEMENT)
async def accept_announcement(
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
            ADMIN_PERMISSIONS.MANAGE_ANNOUNCEMENTS
        ]
    )

    result = DataStructure()

    return result

@admin_router.post(AdminEndpoints.DECLINE_ANNOUNCEMENT)
async def decline_announcement(
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
            ADMIN_PERMISSIONS.MANAGE_ANNOUNCEMENTS
        ]
    )

    result = DataStructure()

    return result

@admin_router.post(AdminEndpoints.DELETE_ANNOUNCEMENT)
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

    return result