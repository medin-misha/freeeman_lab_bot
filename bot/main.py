from handlers import main_router
from aiogram import Bot, Dispatcher, types
import asyncio
import logging
from config import settings

BOT_TOKEN = settings.token
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def main():
    logging.basicConfig(level=logging.DEBUG)
    dp.include_router(main_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
