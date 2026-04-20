import logging
from typing import Any

from aiogram import Bot

from config import settings
from core.rmq import broker


logger = logging.getLogger(__name__)
_bot: Bot | None = None


def set_bot_instance(bot: Bot) -> None:
    global _bot
    _bot = bot


@broker.subscriber(settings.nucleus_application_queue)
async def handle_nucleus_application(message: object) -> None:
    if _bot is None:
        logger.error("Bot instance is not configured for nucleus application consumer")
        return

    username = _extract_text(message, "username") or "не указан"
    provided_name = _extract_text(message, "provided_name")
    first_name = _extract_text(message, "first_name")
    last_name = _extract_text(message, "last_name")
    application_text = _extract_text(message, "application_text") or "Пусто"
    submitted_at = _extract_text(message, "submitted_at") or "Не указано"
    full_name = provided_name or " ".join(
        part for part in [first_name, last_name] if part
    ) or "не указаны"

    notification_text = settings.message.text.get("notifications", {}).get(
        "nucleus_application",
        (
            "Новая заявка в «Ядро»\n\nUsername: {username}\n"
            "Имя / фамилия: {full_name}\nДата / время: {submitted_at}\n\n"
            "Теĸст заявĸи:\n{application_text}"
        ),
    ).format(
        username=username,
        full_name=full_name,
        submitted_at=submitted_at,
        application_text=application_text,
    )

    for chat_id in settings.chat_ids_list:
        try:
            await _bot.send_message(chat_id=chat_id, text=notification_text)
        except Exception:
            logger.exception(
                "Failed to send nucleus application notification to chat_id=%s",
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
