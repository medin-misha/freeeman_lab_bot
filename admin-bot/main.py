import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import settings
from handlers import main_router
from handlers.events.diagnostics import broker as diagnostic_broker
from handlers.events.diagnostics import set_bot_instance as set_diagnostic_bot_instance


BOT_TOKEN = settings.token
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    dp.include_router(main_router)
    set_diagnostic_bot_instance(bot)
    await diagnostic_broker.start()
    try:
        await dp.start_polling(bot)
    finally:
        await diagnostic_broker.close()


if __name__ == "__main__":
    asyncio.run(main())
