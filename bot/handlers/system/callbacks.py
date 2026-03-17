from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from core.utils import check_sub_channel
from core.buttons import start_callback_reply
from config import settings

router = Router(name="system_callbacks")

@router.callback_query(F.data == settings.message.text.get("callback").get("check_subscribe"))
async def check_subscribe_callback(query: CallbackQuery, bot: Bot):
    if await check_sub_channel(bot=bot, user_id=query.from_user.id):
        await query.answer(text="Теперь напиши МАСШТАБ")
        await query.message.reply(text="Прекрасно, теперь напиши 'МАСШТАБ'", reply_markup=start_callback_reply())
    else:
        await query.answer(text="Нужно войти в сообщество")