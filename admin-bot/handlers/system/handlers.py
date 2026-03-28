from aiogram import F, Router, types
from aiogram.filters import CommandStart

from config import settings


router = Router(name="system")
router.message.filter(F.chat.id.in_(settings.chat_ids_list))


@router.message(CommandStart())
async def start_handler(msg: types.Message) -> None:
    await msg.answer(settings.message.text.get("start", "Admin bot active"))
