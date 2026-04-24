import logging
from typing import Any

from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import settings
from core.rmq import broker

logger = logging.getLogger(__name__)
_bot: Bot | None = None


def set_bot_instance(bot: Bot) -> None:
    global _bot
    _bot = bot


@broker.subscriber(settings.mentorship_request_queue)
async def handle_mentorship_request(message: object) -> None:
    if _bot is None:
        logger.error("Bot instance is not configured for mentorship request consumer")
        return

    username = _extract_text(message, "username") or "не указан"

    notification_text = settings.message.text.get("notifications", {}).get(
        "mentorship_request",
        "<b>Новый запрос на наставничество</b>\n\n<b>Username:</b> {username}",
    ).format(username=username)

    reply_markup = None
    if username != "не указан":
        clean_username = username.lstrip("@")
        reply_markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=f"@{clean_username}", url=f"https://t.me/{clean_username}")]
            ]
        )

    for chat_id in settings.chat_ids_list:
        try:
            await _bot.send_message(chat_id=chat_id, text=notification_text, reply_markup=reply_markup)
        except Exception:
            logger.exception(
                "Failed to send mentorship request notification to chat_id=%s",
                chat_id,
            )


def _extract_text(message: object, field_name: str) -> str | None:
    value = _extract_value(message, field_name)
    if isinstance(value, str):
        normalized = value.strip()
        return normalized or None
    return None


def _extract_value(message: object, field_name: str) -> Any:
    if isinstance(message, dict):
        return message.get(field_name)
    if hasattr(message, field_name):
        return getattr(message, field_name)
    return None
