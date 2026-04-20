from __future__ import annotations

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


@broker.subscriber(settings.analysis_schedule_confirmation_queue)
async def handle_analysis_schedule_confirmation(message: object) -> None:
    if _bot is None:
        logger.error(
            "Bot instance is not configured for analysis schedule confirmation consumer"
        )
        return

    format_name = _extract_text(message, "analysis_format")
    if format_name == "private":
        format_label = "приватный"
    else:
        format_label = "публичный"

    confirmed_at = _extract_text(message, "confirmed_at") or "Не указано"

    notification_text = settings.message.text.get("notifications", {}).get(
        "analysis_schedule_confirmation",
        (
            "Новая запись на разбор\n\n"
            "Формат разбора: {format_label}\n"
            "● анкета заполнена\n"
            "● расписание подтверждено\n"
            "● дата / время: {confirmed_at}"
        ),
    ).format(
        format_label=format_label,
        confirmed_at=confirmed_at,
    )

    for chat_id in settings.chat_ids_list:
        try:
            await _bot.send_message(chat_id=chat_id, text=notification_text)
        except Exception:
            logger.exception(
                "Failed to send analysis schedule confirmation to chat_id=%s",
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
