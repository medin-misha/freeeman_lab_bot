from aiogram import Bot
from config import settings

async def check_sub_channel(bot: Bot, user_id: int) -> bool:
    member = await bot.get_chat_member(
        chat_id=settings.channel_id,
        user_id=user_id
    )
    if member.status != "left":
        return True
    else:
        return False