from functools import wraps
from classes.api_requests import UserAPI, AdminAPI
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import Message
from typing import Any, Callable


class CheckRegistered:

    def __call__(
            self,
            check_banned: bool = True
    ) -> Any:

        def handler(func: Callable) -> Callable:

            @wraps(func)
            async def wrapper(*args, **kwargs) -> Any:
                state: FSMContext = kwargs["state"]
                response = await UserAPI.get_user(
                    0, telegram_id=state.user
                )

                from handlers.user import signup

                if not response._success:
                    if response.data:
                        if response.data.is_banned:

                            return await signup.banned_menu(
                                *args, **kwargs
                            )

                    return await signup.welcome(
                        *args, **kwargs
                    )

                return await func(
                    *args, **kwargs
                )

            return wrapper

        return handler


def private_message(func: Callable) -> Callable:

    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        message: Message = args[0]

        if message.chat.type == "private":

            return await func(
                *args, **kwargs
            )

    return wrapper


check_registered = CheckRegistered()

