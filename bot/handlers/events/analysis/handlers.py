from aiogram import F, Router
from aiogram.types import FSInputFile, Message
from config import settings

from .buttons import analysis_format_inline_keyboard, wording_of_request_for_analysis_inline_keyboard

router = Router(name="analysis_handlers")


@router.message(F.text.lower() == "разбор")
async def analysis_handler(msg: Message) -> None:
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action="upload_document")
    await msg.bot.send_document(
        chat_id=msg.chat.id,
        document=FSInputFile(settings.files.wording_of_request_for_analysis),
        caption=settings.message.text.get("wording_of_request_for_analysis"),
        reply_markup=wording_of_request_for_analysis_inline_keyboard(),
    )

@router.message(F.text.lower() == "я готов к разбору!")
async def analysis_handler(msg: Message) -> None:
    await msg.answer(
        text=settings.message.text.get("handler"),
        reply_markup=analysis_format_inline_keyboard(),
    )
