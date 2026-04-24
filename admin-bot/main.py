import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer

from config import settings
from handlers import main_router
from handlers.events.analysis import set_bot_instance as set_analysis_bot_instance
from handlers.events.consultations import set_bot_instance as set_consultations_bot_instance
from handlers.events.mentorship import set_bot_instance as set_mentorship_bot_instance
from handlers.events.regressions import set_bot_instance as set_regressions_bot_instance
from handlers.events.diagnostics import broker as diagnostic_broker
from handlers.events.diagnostics import set_bot_instance as set_diagnostic_bot_instance
from handlers.events.nucleus import set_bot_instance as set_nucleus_bot_instance


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
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    session=session,
)
dp = Dispatcher()


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    dp.include_router(main_router)
    set_analysis_bot_instance(bot)
    set_consultations_bot_instance(bot)
    set_mentorship_bot_instance(bot)
    set_regressions_bot_instance(bot)
    set_diagnostic_bot_instance(bot)
    set_nucleus_bot_instance(bot)
    await diagnostic_broker.start()
    try:
        await dp.start_polling(bot)
    finally:
        await diagnostic_broker.close()


if __name__ == "__main__":
    asyncio.run(main())
