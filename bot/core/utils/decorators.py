from functools import wraps

from core.buttons import start_inline_keyboard

from .funcs import check_sub_channel
from .api import UserAPI, get_or_create_user


def check_sub_channel_dec(func):
    @wraps(func)
    async def wrapped_func(*args, **kwargs):
        msg = args[0]
        bot = msg.bot

        if await check_sub_channel(bot=bot, user_id=msg.from_user.id):
            return await func(*args, **kwargs)

        await msg.answer(
            text="Нужно войти в сообщество",
            reply_markup=start_inline_keyboard(),
        )

    return wrapped_func


def ensure_user_registered(func):
    """
    Декоратор для aiogram-обработчиков.
    Проверяет наличие пользователя в БД по chat_id.
    Если пользователя нет — регистрирует его перед вызовом обработчика.
    """
    @wraps(func)
    async def wrapped_func(*args, **kwargs):
        msg = args[0]
        from_user = msg.from_user
        if from_user is not None:
            await get_or_create_user(
                chat_id=str(from_user.id),
                from_user=from_user,
                user_api=UserAPI(),
            )
        return await func(*args, **kwargs)

    return wrapped_func
