from aiogram import Router, types, F
from aiogram.types import FSInputFile
from config import settings
from core.buttons import mashtab_inline, analysis_reply

router = Router(name="events")

@router.message(F.text.lower() == "масштаб")
async def mashtab_handler(msg: types.Message):
    await msg.bot.send_chat_action(
        chat_id=msg.chat.id,
        action="upload_document"
    )
    # await msg.reply_document(
    #     document=FSInputFile(path=settings.files.scale_file_pdf),
    # )
    # await msg.reply_document(
    #     document=FSInputFile(path=settings.files.scale_file_epub),
    # )
    await msg.reply(
        text=settings.message.text.get("scale"),
        reply_markup=mashtab_inline()
    )
    await msg.answer(
        text=settings.message.text.get("scale2"),
        reply_markup=analysis_reply()
    )


@router.message(F.text.lower() == "разбор")
async def analysis_handler(msg: types.Message):
    await msg.reply(
        text=settings.message.text.get("analysis")
    )
    await msg.reply_document(
        document=FSInputFile(path=settings.files.analysis_file_pdf),
    )