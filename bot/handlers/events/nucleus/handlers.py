from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import settings
from core.utils import ensure_user_registered

from .buttons import nucleus_mini_app_inline_keyboard


router = Router(name="nucleus_handlers")


@router.message(F.text.lower().in_(("ядро", "узнать про «ядро»", "узнать про ядро")))
@ensure_user_registered
async def nucleus_entry_handler(msg: Message, state: FSMContext) -> None:
    await state.clear()
    await msg.answer(
        text=settings.message.text.get("nucleus_intro"),
        reply_markup=nucleus_mini_app_inline_keyboard(),
    )
