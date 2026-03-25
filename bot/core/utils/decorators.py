from functools import wraps

from core.buttons import start_inline_keyboard

from .funcs import check_sub_channel


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
