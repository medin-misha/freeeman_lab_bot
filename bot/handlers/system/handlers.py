import logging

from aiogram import Router, types
from aiogram.filters import CommandStart

from config import settings
from core.buttons import start_inline
from core.utils import UserAPI

router = Router(name="system")
user_api = UserAPI()

@router.message(CommandStart())
async def start_handler(msg: types.Message) -> None:
    await msg.answer(settings.message.text.get("start"), reply_markup=start_inline())
    user = msg.from_user

    if user is not None:
        try:
            await user_api.add_user(
                username=user.username,
                email=None,
                phone=None,
                first_name=user.first_name,
                last_name=user.last_name,
                chat_id=str(user.id),
            )
        except Exception:
            logging.exception("Failed to register user %s", user.id)
