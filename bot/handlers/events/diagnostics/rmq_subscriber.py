import logging
from typing import Any

from aiogram import Bot
from aiogram.types import BufferedInputFile
from faststream.rabbit import RabbitBroker

from config import settings
from core.utils.api import FileAPI

from .buttons import diagnostic_success_reply_keyboard

logger = logging.getLogger(__name__)

broker = RabbitBroker(settings.rmq_url)
_bot: Bot | None = None


def set_bot_instance(bot: Bot) -> None:
    global _bot
    _bot = bot


@broker.subscriber(settings.diagnostic_response_queue)
async def handle_diagnostic_response(message: object) -> None:
    chat_id = _extract_chat_id(message)
    file_id = _extract_file_id(message)

    if chat_id is None:
        logger.warning("Diagnostic response event does not contain chat_id: %r", message)
        return

    if file_id is None:
        logger.warning("Diagnostic response event does not contain file_id: %r", message)
        return

    if _bot is None:
        logger.error("Bot instance is not configured for diagnostic response consumer")
        return

    try:
        downloaded_file = await FileAPI().download_file(file_id)
        await _bot.send_message(chat_id, "Ваша диагностика готова!")
        await _bot.send_document(
            chat_id=chat_id,
            document=BufferedInputFile(
                downloaded_file.content,
                filename=downloaded_file.filename,
            ),
        )
        await _bot.send_message(chat_id, "Теперь вам доступен разбор. Нажмите кнопку 'Разбор' для получения доступа к нему!", reply_markup=diagnostic_success_reply_keyboard())
    except Exception:
        logger.exception(
            "Failed to deliver diagnostic file_id=%s to chat_id=%s",
            file_id,
            chat_id,
        )


def _extract_chat_id(message: object) -> str | None:
    value = _extract_value(message, "chat_id")
    if value is None:
        return None

    if isinstance(value, int):
        return str(value)

    if isinstance(value, str):
        chat_id = value.strip()
        return chat_id or None

    return None


def _extract_file_id(message: object) -> int | None:
    value = _extract_value(message, "file_id")
    if isinstance(value, int):
        return value

    if isinstance(value, str) and value.isdigit():
        return int(value)

    return None


def _extract_value(message: object, field_name: str) -> Any:
    if isinstance(message, dict):
        return message.get(field_name)

    if hasattr(message, field_name):
        return getattr(message, field_name)

    return None
