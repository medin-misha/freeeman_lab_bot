import logging

from aiogram import Bot, Router
from aiogram.types import ErrorEvent, Message

from config import settings
from .exceptions import SupportRequiredError, UserFacingError

router = Router(name="errors")
logger = logging.getLogger(__name__)


def _extract_chat_id(event: ErrorEvent) -> int | None:
    update = event.update

    if update.message:
        return update.message.chat.id
    if update.callback_query and update.callback_query.message:
        return update.callback_query.message.chat.id

    return None


@router.error()
async def error_handler(event: ErrorEvent, bot: Bot) -> None:
    errors_text = settings.message.text.get("errors", {})
    exception = event.exception
    chat_id = _extract_chat_id(event)

    if isinstance(exception, UserFacingError):
        logger.warning(
            "User-facing error for chat_id=%s message_key=%s detail=%s",
            chat_id,
            exception.message_key,
            exception.detail,
        )
        message_text = exception.resolve_message(errors_text)
    else:
        if isinstance(exception, SupportRequiredError):
            logger.error(
                "Support-required error for chat_id=%s endpoint=%s status=%s detail=%s",
                chat_id,
                exception.endpoint,
                exception.status_code,
                exception.detail,
                exc_info=exception,
            )
        else:
            logger.error(
                "Unhandled error for chat_id=%s",
                chat_id,
                exc_info=exception,
            )
        message_text = (
            errors_text.get("server_error")
            or errors_text.get("non_flow_error")
            or "На стороне сервера произошла ошибка. Пожалуйста, обратитесь в поддержку."
        )

    if chat_id is not None:
        try:
            await bot.send_message(chat_id=chat_id, text=message_text)
        except Exception as err:
            logger.error(
                "Failed to deliver error message to chat_id=%s",
                chat_id,
                exc_info=err,
            )

@router.message()
async def any_message_handler(msg: Message) -> None:
    await msg.answer(
        text=settings.message.text.get("errors").get("any_massage_text"),
    )
