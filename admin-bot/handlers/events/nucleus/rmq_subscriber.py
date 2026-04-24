import logging
from html import escape
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


@broker.subscriber(settings.nucleus_application_queue)
async def handle_nucleus_application(message: object) -> None:
    if _bot is None:
        logger.error("Bot instance is not configured for nucleus application consumer")
        return

    username = _extract_text(message, "username") or "не указан"
    priorities = _format_priorities(_extract_value(message, "priorities"))

    notification_text = settings.message.text.get("notifications", {}).get(
        "nucleus_application",
        (
            "Новая заявка в «Ядро»\n\n"
            "Чем занимаешься:\n<blockquote>{activity}</blockquote>\n"
            "Запрос:\n<blockquote>{request}</blockquote>\n"
            "Приоритеты:\n{priorities}\n"
            "Мотивация:\n<blockquote>{motivation}</blockquote>\n"
            "Трудности:\n<blockquote>{difficulties}</blockquote>\n"
            "Включённость:\n<blockquote>{readiness}</blockquote>\n"
            "Время в неделю:\n<blockquote>{weekly_time}</blockquote>\n"
            "Правила:\n<blockquote>{rules}</blockquote>\n"
            "Оплата:\n<blockquote>{payment}</blockquote>"
        ),
    ).format(
        activity=_html(_extract_text(message, "activity") or "не указано"),
        request=_html(_extract_text(message, "request") or "не указано"),
        priorities=priorities,
        motivation=_html(_extract_text(message, "motivation") or "не указано"),
        difficulties=_html(_extract_text(message, "difficulties") or "не указано"),
        readiness=_html(_extract_text(message, "readiness") or "не указано"),
        weekly_time=_html(_extract_text(message, "weekly_time") or "не указано"),
        rules=_html(_extract_text(message, "rules") or "не указано"),
        payment=_html(_extract_text(message, "payment") or "не указано"),
    )

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
                "Failed to send nucleus application notification to chat_id=%s",
                chat_id,
            )


def _extract_text(message: object, field_name: str) -> str | None:
    value = _extract_value(message, field_name)
    if isinstance(value, str):
        normalized = value.strip()
        return normalized or None

    return None


def _format_priorities(value: Any) -> str:
    if isinstance(value, list):
        items = [_html(str(item).strip()) for item in value if str(item).strip()]
        return "\n".join(f"• {item}" for item in items) if items else "не указано"

    if isinstance(value, str):
        normalized = value.strip()
        return _html(normalized) if normalized else "не указано"

    return "не указано"


def _html(value: str) -> str:
    return escape(value, quote=False)


def _extract_value(message: object, field_name: str) -> Any:
    if isinstance(message, dict):
        return message.get(field_name)

    if hasattr(message, field_name):
        return getattr(message, field_name)

    return None
