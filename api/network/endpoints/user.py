from fastapi import (
    APIRouter,
    Depends,
    Response,
    Request,
    Query,
)
from typing_extensions import Annotated
from datetime import datetime
from typing import Union, AsyncIterable
from starlette import status as HTTPStatus
from sqlalchemy import select, update, BigInteger
from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from database.core import (
    core
)
from database.models.models import (
    Users,
    Announcements,
    Notifications
)
from common.dto.user import (
    UserCreate,
    UserUpdate,
    NotificationSend
)
from common.dto.announcement import (
    AddAnnouncement
)
from schemas.schemas import (
    BaseUser,
    BaseAnnouncement,
    UserAnnouncementsResponse,
    BaseNotification
)
from schemas.classes import (
    UserEndpoints,
    AnnouncementStatus,
    AnnouncementSort,
    UserMode
)
from services import exceptions
from services.errors_reporter import Reporter
from schemas.base import DataStructure
from utils import utils
from utils.utils import OAuth2


user_router = APIRouter()


@user_router.post(UserEndpoints.CREATE_USER)
async def create_user(
        parameters: UserCreate,
        request: Request,
        session: AsyncSession = Depends(
            core.create_sa_session
        )
) -> Union[DataStructure]:
    await OAuth2._check_token(
        request,
        session
    )
    result = DataStructure()

    data_scheme = BaseUser().model_validate(
        parameters.model_dump()
    )
    user = await session.get(
        Users,
        parameters.telegram_id
    )

    if user:
        return await Reporter(
            exception=exceptions.ItemExists,
            message="User already exist"
        )._report()

    data_scheme.created_at = utils.timestamp()

    session.add(
        Users(
            **data_scheme.model_dump(
                exclude={
                    "is_banned"
                }
            )
        )
    )

    await session.commit()
    await session.close()

    result.data = data_scheme.model_dump()
    result._status = HTTPStatus.HTTP_201_CREATED

    return result


@user_router.get(UserEndpoints.GET_USER)
async def get_user(
        telegram_id: int,
        request: Request,
        session: AsyncSession = Depends(
            core.create_sa_session
        )
) -> Union[DataStructure]:
    await OAuth2._check_token(
        request,
        session
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

    await session.close()

    user_model = user.as_model()
    user_model.is_banned = (
        await OAuth2._check_banned(
            telegram_id,
            session
        )
    )._success

    result.data = user_model.model_dump()
    result._status = HTTPStatus.HTTP_200_OK

    return result


@user_router.patch(UserEndpoints.UPDATE_USER)
async def update_user(
        telegram_id: int,
        parameters: UserUpdate,
        request: Request,
        session: AsyncSession = Depends(
            core.create_sa_session
        )
) -> Union[DataStructure]:
    await OAuth2._check_token(
        request,
        session
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

    user.validate(
        parameters.model_dump(
            exclude_defaults=True
        )
    )
    await session.commit()
    await session.close()

    user_model = user.as_model()
    user_model.is_banned = (
        await OAuth2._check_banned(
            telegram_id,
            session
        )
    )._success

    result.data = user_model.model_dump()
    result._status = HTTPStatus.HTTP_200_OK

    return result


@user_router.post(UserEndpoints.ADD_ANNOUNCEMENT)
async def add_annoucement(
        telegram_id: int,
        parameters: AddAnnouncement,
        request: Request,
        session: AsyncSession = Depends(
            core.create_sa_session
        )
) -> Union[DataStructure]:
    token = await OAuth2._check_token(
        request,
        session
    )
    result = DataStructure()

    if token.id_ != telegram_id:
        return await Reporter(
            exception=exceptions.NoAccess,
            message="Only the account owner have permissions to place the announcements"
        )._report()

    is_banned = await OAuth2._check_banned(
        telegram_id,
        session
    )

    if is_banned:
        return await Reporter(
            exception=exceptions.NoAccess,
            message="Banned users cannot add announcements"
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

    data_scheme = BaseAnnouncement().model_validate(
        parameters.model_dump()
    )
    data_scheme.owner_id = telegram_id
    data_scheme.announcement_id = utils._uuid()
    data_scheme.status = AnnouncementStatus.PENDING

    session.add(
        Announcements(
            **data_scheme.model_dump()
        )
    )
    await session.commit()
    await session.close()

    result.data = data_scheme.model_dump()
    result._status = HTTPStatus.HTTP_201_CREATED

    return result


@user_router.get(UserEndpoints.GET_USER_ANNOUNCEMENTS)
async def get_user_announcements(
        request: Request,
        telegram_id: int,
        mode: int = Query(
            0,
            gt=-1,
            lt=2
        ),
        status: int = Query(
            0,
            gt=-1,
            lt=3
        ),
        limit: int = Query(
            1,
            gt=0
        ),
        page: int = 0,
        session: AsyncSession = Depends(
            core.create_sa_session
        )
) -> Union[DataStructure]:
    await OAuth2._check_token(
        request,
        session
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

    document = UserAnnouncementsResponse(
        status=status,
        page=page
    )
    query_result = await session.execute(
        select(
            Announcements
        ).filter(
            Announcements.owner_id == telegram_id
        ).filter(
            Announcements.mode == mode
        ).order_by(
            Announcements.timestamp.desc()
        )
    )

    announcements: dict = {}
    offset: int = page * limit

    for i, announcement in enumerate(query_result.scalars().all()):

        match announcement.status:
            case 0:
                document.order.active += 1
            case 1:
                document.order.completed += 1
            case 2:
                document.order.pending += 1

        if not i % limit:
            document.pages += 1

        if i in range(
                offset,
                offset + limit
        ):
            if announcement.status == status:
                announcements.update(
                    {
                        announcement.announcement_id: announcement.as_dict()
                    }
                )

    result.data.update(
        {
            "announcements": announcements,
            "document": document
        }
    )
    result._status = HTTPStatus.HTTP_200_OK

    return result


@user_router.get(UserEndpoints.GET_NOTIFICATIONS)
async def get_notifications(
        request: Request,
        telegram_id: int,
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
        session
    )
    result = DataStructure()

    await OAuth2._check_ownership(
        telegram_id,
        request
    )

    query_result = await session.get(
        Notifications,
        telegram_id
    )

    if not query_result:
        return await Reporter(
            exception=exceptions.ItemNotFound,
            message="User not found"
        )._report()

    notifications: dict = {}
    offset: int = page * limit

    for i, (v, k) in enumerate(query_result.content.items()):
        if i in range(
                offset,
                offset + limit
        ):
            notifications.update(
                {
                    v: k
                }
            )

    await session.close()

    result.data.update(
        {
            "notifications": notifications,
            "details": query_result.details
        }
    )
    result._status = HTTPStatus.HTTP_200_OK

    return result


@user_router.post(UserEndpoints.SEND_NOTIFICATION)
async def send_notification(
        telegram_id: int,
        parameters: NotificationSend,
        request: Request,
        session: AsyncSession = Depends(
            core.create_sa_session
        )
) -> Union[DataStructure]:
    await OAuth2._check_token(
        request,
        session
    )
    result = DataStructure()

    notifications = await session.get(
        Notifications,
        telegram_id
    )

    if not notifications:
        return await Reporter(
            exception=exceptions.ItemNotFound,
            message="User not found"
        )._report()

    notification = BaseNotification().model_validate(
        parameters.model_dump()
    )
    notification.id_ = notifications.details["last_id"] + 1
    notification.date = utils.timestamp()

    notifications.content[notification.id_] = notification.model_dump()
    notifications.details["last_id"] = notification.id_

    await session.execute(
        update(
            Notifications
        ).filter(
            Notifications.telegram_id == telegram_id
        ).values(
            {
                "details": notifications.details,
                "content": notifications.content
            }
        )
    )

    await session.commit()
    await session.close()

    result.message = "The notification was sent successfully"
    result._status = HTTPStatus.HTTP_200_OK

    return result


@user_router.get(UserEndpoints.GET_NOTIFICATION)
async def get_notification(
        telegram_id: int,
        notification_id: int,
        request: Request,
        session: AsyncSession = Depends(
            core.create_sa_session
        )
) -> Union[DataStructure]:
    await OAuth2._check_token(
        request,
        session
    )
    result = DataStructure()

    await OAuth2._check_ownership(
        telegram_id,
        request
    )

    notifications = await session.get(
        Notifications,
        telegram_id
    )

    if not notifications:
        return await Reporter(
            exception=exceptions.ItemNotFound,
            message="User not found"
        )._report()

    if notifications.details["last_id"] > notification_id:
        return await Reporter(
            exception=exceptions.ItemNotFound,
            message="Notification not found"
        )

    result.data = notifications.content[
        notification_id
    ]
    result._status = HTTPStatus.HTTP_200_OK

    return result


@user_router.patch(UserEndpoints.READ_NOTIFICATION)
async def read_notification(
        telegram_id: int,
        notification_id: int,
        request: Request,
        session: AsyncSession = Depends(
            core.create_sa_session
        )
) -> Union[DataStructure]:
    await OAuth2._check_token(
        request,
        session
    )
    result = DataStructure()

    await OAuth2._check_ownership(
        telegram_id,
        request
    )

    notifications = await session.get(
        Notifications,
        telegram_id
    )

    if not notifications:
        return await Reporter(
            exception=exceptions.ItemNotFound,
            message="User not found"
        )._report()

    if notification_id > notifications.details["last_id"] or notification_id < 1:
        return await Reporter(
            exception=exceptions.ItemNotFound,
            message="Notification not found"
        )._report()

    notifications.content[f"{notification_id}"]["unread"] = False

    await session.execute(
        update(
            Notifications
        ).filter(
            Notifications.telegram_id == telegram_id
        ).values(
            {
                "content": notifications.content
            }
        )
    )
    await session.commit()
    await session.close()

    result._status = HTTPStatus.HTTP_200_OK

    return result


