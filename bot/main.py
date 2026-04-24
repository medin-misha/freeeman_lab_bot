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
from handlers.events.analysis.publisher import broker as analysis_broker
from handlers.events.more.publisher import broker as consultations_broker

logger = logging.getLogger(__name__)

BOT_TOKEN = settings.token


def build_session() -> AiohttpSession:
    telegram_bot_api_url = settings.telegram_bot_api_url.strip().rstrip("/")
    if not telegram_bot_api_url or telegram_bot_api_url == "https://api.telegram.org":
        return AiohttpSession()

    return AiohttpSession(
        api=TelegramAPIServer.from_base(
            telegram_bot_api_url,
            is_local=True,
        )
    )


session = build_session()
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML), session=session)
dp = Dispatcher()



async def main():
    logging.basicConfig(level=logging.INFO)
    try:
        dp.include_router(main_router)
        set_diagnostic_bot_instance(bot)
        await diagnostic_broker.start()
        try:
            await analysis_broker.start()
            try:
                await consultations_broker.start()
                try:
                    await dp.start_polling(bot)
                finally:
                    await consultations_broker.close()
            finally:
                await analysis_broker.close()
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
