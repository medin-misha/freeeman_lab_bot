from handlers import main_router
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer

import asyncio
import logging
from config import settings
from handlers.events.diagnostics import broker as diagnostic_broker
from handlers.events.diagnostics import set_bot_instance as set_diagnostic_bot_instance
from handlers.events.nucleus import broker as nucleus_broker

logger = logging.getLogger(__name__)

BOT_TOKEN = settings.token
session = AiohttpSession(
    api=TelegramAPIServer.from_base(
        settings.telegram_bot_api_url,
        is_local=True,
    )
)
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML), session=session)
dp = Dispatcher()



async def main():
    logging.basicConfig(level=logging.INFO)
    try:
        dp.include_router(main_router)
        set_diagnostic_bot_instance(bot)
        await diagnostic_broker.start()
        try:
            await nucleus_broker.start()
            try:
                await dp.start_polling(bot)
            finally:
                await nucleus_broker.close()
        finally:
            await diagnostic_broker.close()
    except Exception:
        logger.exception("Critical error, bot stopped")
        raise


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception:
        logging.exception("Bot process terminated with error")
