from aiogram import Bot, F, Router
from aiogram.types import CallbackQuery, FSInputFile

from config import settings
from .buttons import start_reply_keyboard
from core.utils import check_sub_channel, ensure_user_registered

router = Router(name="system_callbacks")


@router.callback_query(F.data == settings.message.text.get("callback").get("check_subscribe"))
@ensure_user_registered
async def check_subscribe_callback(query: CallbackQuery, bot: Bot):
    if await check_sub_channel(bot=bot, user_id=query.from_user.id):
        await query.answer()
        await query.message.bot.send_chat_action(
            chat_id=query.message.chat.id,
            action="upload_photo",
        )
        await query.message.answer_photo(
            photo=FSInputFile(path=settings.files.subscribe_preview_image),
        )
        await query.message.bot.send_chat_action(
            chat_id=query.message.chat.id,
            action="upload_video",
        )
        await query.message.answer_video(
            video=FSInputFile(path=settings.files.subscribe_video),
        )
        await query.message.answer(
            text=settings.message.text.get("subscribe_success"),
            reply_markup=start_reply_keyboard(),
        )
    else:
        await query.answer(text="Я поĸа не вижу подписĸу на сообщество. Подпишись и снова нажми ĸнопĸу ниже.")
