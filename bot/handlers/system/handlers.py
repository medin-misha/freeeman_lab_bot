from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from config import settings
from core.buttons import start_inline_keyboard
from core.utils import UserAPI, get_or_create_user

router = Router(name="system")
user_api = UserAPI()


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
