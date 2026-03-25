from aiogram import F, Router, types
from aiogram.types import FSInputFile

from config import settings
from core.buttons import (
    analysis_reply_keyboard,
    scale_inline_keyboard,
)
from core.utils import check_sub_channel_dec

router = Router(name="scale_handlers")


@router.message(F.text.lower() == "масштаб")
@check_sub_channel_dec
async def mashtab_handler(msg: types.Message):
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action="upload_document")
    await msg.reply_document(
        document=FSInputFile(path=settings.files.scale_file_pdf),
    )
    await msg.reply_document(
        document=FSInputFile(path=settings.files.scale_file_epub),
    )
    await msg.reply(
        text=settings.message.text.get("scale"),
        reply_markup=scale_inline_keyboard(),
    )
    await msg.answer(
        text=settings.message.text.get("scale2"),
        reply_markup=analysis_reply_keyboard(),
    )
