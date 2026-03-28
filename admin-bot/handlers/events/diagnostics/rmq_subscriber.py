import logging

from aiogram import Bot
from aiogram.types import BufferedInputFile
from faststream.rabbit import RabbitBroker

from config import settings
from core.utils import (
    DownloadedFile,
    FileAPI,
    UserAPI,
    build_display_name,
    extract_diagnostic_id,
    extract_file_id,
    extract_user_id,
)

from .buttons import send_result_inline_keyboard


logger = logging.getLogger(__name__)

broker = RabbitBroker(settings.rmq_url)
_bot: Bot | None = None

user_api = UserAPI()
file_api = FileAPI()


def set_bot_instance(bot: Bot) -> None:
    global _bot
    _bot = bot


@broker.subscriber(settings.diagnostic_request_queue)
async def handle_diagnostic_request(message: object) -> None:
    diagnostic_id = extract_diagnostic_id(message)
    file_id = extract_file_id(message)
    user_id = extract_user_id(message)

    if diagnostic_id is None:
        logger.warning("Diagnostic event does not contain diagnostic id: %r", message)
        return

    if file_id is None:
        logger.warning("Diagnostic event does not contain file_id: %r", message)
        return

    if user_id is None:
        logger.warning("Diagnostic event does not contain user_id: %r", message)
        return

    if _bot is None:
        logger.error("Bot instance is not configured for diagnostic request consumer")
        return

    try:
        logger.info(
            "Received diagnostic event with diagnostic_id=%s user_id=%s file_id=%s, notifying %s chats",
            diagnostic_id,
            user_id,
            file_id,
            len(settings.chat_ids_list),
        )
        user = await user_api.get_user(user_id)
        downloaded_file = await file_api.download_file(file_id)
        notification_text = settings.message.text.get("notifications", {}).get(
            "diagnostic_request",
            "Пользователь ({display_name}) хочет пройти диагностику",
        ).format(
            display_name=build_display_name(user.username, user_id),
            user_id=user_id,
        )
        reply_markup = send_result_inline_keyboard(diagnostic_id, user_id)
        await _broadcast_message(notification_text, reply_markup)
        await _broadcast_voice(downloaded_file)
    except Exception:
        logger.exception(
            "Failed to process diagnostic event for diagnostic_id=%s user_id=%s file_id=%s",
            diagnostic_id,
            user_id,
            file_id,
        )


async def _broadcast_message(
    text: str,
    reply_markup: object,
) -> None:
    if _bot is None:
        return

    for chat_id in settings.chat_ids_list:
        try:
            await _bot.send_message(chat_id, text, reply_markup=reply_markup)
        except Exception:
            logger.exception("Failed to send Telegram message to chat_id=%s", chat_id)


async def _broadcast_voice(downloaded_file: DownloadedFile) -> None:
    if _bot is None:
        return

    for chat_id in settings.chat_ids_list:
        try:
            await _bot.send_voice(
                chat_id=chat_id,
                voice=BufferedInputFile(
                    downloaded_file.content,
                    filename=downloaded_file.filename,
                ),
            )
        except Exception:
            logger.exception("Failed to send Telegram voice to chat_id=%s", chat_id)
