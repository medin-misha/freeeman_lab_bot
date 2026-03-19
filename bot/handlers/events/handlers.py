from aiogram import Router, types, F, Bot
from aiogram.types import FSInputFile
from config import settings
from core.utils import check_sub_channel_dec
from core.buttons import (
    analysis2_reply,
    analysis_reply,
    handling_reply,
    handling_inline,
    mashtab_inline,
    analysis_inline,
    start_inline,
)

router = Router(name="events")

@router.message(F.text.lower() == "масштаб")
@check_sub_channel_dec
async def mashtab_handler(msg: types.Message, bot: Bot):
    await msg.bot.send_chat_action(
        chat_id=msg.chat.id,
        action="upload_document"
    )
    await msg.reply_document(
        document=FSInputFile(path=settings.files.scale_file_pdf),
    )
    await msg.reply_document(
        document=FSInputFile(path=settings.files.scale_file_epub),
    )
    await msg.reply(
        text=settings.message.text.get("scale"),
        reply_markup=mashtab_inline()
    )
    # await msg.answer(
    #     text=settings.message.text.get("scale2"),
    #     reply_markup=analysis_reply()
    # )


# @router.message(F.text.lower() == "диагностика")
@check_sub_channel_dec
async def analysis_handler(msg: types.Message, bot: Bot):
        await msg.reply(
            text=settings.message.text.get("analysis"),
            reply_markup=analysis_inline()
        )
        await msg.reply_document(
            document=FSInputFile(path=settings.files.analysis_file_pdf),
        )
        await msg.reply(
            text=settings.message.text.get("analysis2"), reply_markup=analysis2_reply()
        )

# @router.message(F.text.lower() == "разбор")
@check_sub_channel_dec
async def razbor_handler(msg: types.Message, bot: Bot):
    await msg.answer(
        text=settings.message.text.get("handling"),
        reply_markup=handling_inline(),
    )
