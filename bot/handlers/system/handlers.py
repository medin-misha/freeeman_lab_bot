from aiogram import F, Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from config import settings
from core.utils.global_buttons import start_inline_keyboard
from core.utils import (
    UserAPI,
    check_sub_channel,
    check_sub_channel_dec,
    ensure_user_registered,
    get_or_create_user,
)
from handlers.events.nucleus.buttons import nucleus_mini_app_inline_keyboard
from .buttons import start_reply_keyboard

router = Router(name="system")
user_api = UserAPI()


async def send_main_menu(msg: types.Message, state: FSMContext) -> None:
    await state.clear()
    await msg.answer(
        settings.message.text.get("subscribe_success"),
        reply_markup=start_reply_keyboard(),
    )


def _extract_start_param(text: str | None) -> str | None:
    if not text:
        return None

    parts = text.split(maxsplit=1)
    if len(parts) < 2:
        return None

    return parts[1].strip().lower() or None


@router.message(CommandStart())
async def start_handler(msg: types.Message, state: FSMContext) -> None:
    await state.clear()
    user = msg.from_user

    if user is not None:
        await get_or_create_user(
            chat_id=str(user.id),
            from_user=user,
            user_api=user_api,
        )

        start_param = _extract_start_param(msg.text)
        if start_param == "nucleus" and await check_sub_channel(bot=msg.bot, user_id=user.id):
            await msg.answer(
                text=settings.message.text.get("nucleus_intro"),
                reply_markup=nucleus_mini_app_inline_keyboard(),
            )
            return

    await msg.answer(
        settings.message.text.get("start"),
        reply_markup=start_inline_keyboard(),
    )


@router.message(F.text.lower().in_(("назад", "назад в меню")))
@ensure_user_registered
@check_sub_channel_dec
async def back_to_menu_handler(msg: types.Message, state: FSMContext) -> None:
    await send_main_menu(msg, state)
