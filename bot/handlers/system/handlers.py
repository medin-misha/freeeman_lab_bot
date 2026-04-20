from aiogram import F, Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from config import settings
from core.utils.global_buttons import start_inline_keyboard
from core.utils import (
    UserAPI,
    check_sub_channel_dec,
    ensure_user_registered,
    get_or_create_user,
)
from .buttons import start_reply_keyboard

router = Router(name="system")
user_api = UserAPI()


async def send_main_menu(msg: types.Message, state: FSMContext) -> None:
    await state.clear()
    await msg.answer(
        settings.message.text.get("subscribe_success"),
        reply_markup=start_reply_keyboard(),
    )


@router.message(CommandStart())
async def start_handler(msg: types.Message, state: FSMContext) -> None:
    await state.clear()
    await msg.answer(
        settings.message.text.get("start"),
        reply_markup=start_inline_keyboard(),
    )
    user = msg.from_user

    if user is not None:
        await get_or_create_user(
            chat_id=str(user.id),
            from_user=user,
            user_api=user_api,
        )

@router.message(F.text.lower().in_(("назад", "назад в меню")))
@ensure_user_registered
@check_sub_channel_dec
async def back_to_menu_handler(msg: types.Message, state: FSMContext) -> None:
    await send_main_menu(msg, state)
