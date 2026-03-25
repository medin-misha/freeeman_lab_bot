from aiogram import F, Router, types

from config import settings

from .buttons import analysis_format_inline_keyboard

router = Router(name="analysis_handlers")


@router.message(F.text.lower() == "разбор")
async def analysis_handler(msg: types.Message) -> None:
    await msg.answer(
        text=settings.message.text.get("handler"),
        reply_markup=analysis_format_inline_keyboard(),
    )
