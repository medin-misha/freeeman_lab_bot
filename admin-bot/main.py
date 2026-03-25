import asyncio
import logging
from contextlib import suppress
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from faststream.rabbit import RabbitBroker

from api import BackendAPIClient
from config import settings
from telegram import TelegramBotClient

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

RESULT_CALLBACK_PREFIX = "send_result"
DIAGNOSTIC_STATUS_COMPLETED = "completed"


@dataclass(slots=True)
class PendingResultUpload:
    diagnostic_id: int
    user_id: int


@dataclass(slots=True)
class TelegramAttachment:
    file_id: str
    filename: str
    content_type: str


broker = RabbitBroker(settings.rmq_url)
telegram_client = TelegramBotClient(settings.token)
backend_client = BackendAPIClient(settings.api_url)
allowed_chat_ids = set(settings.chat_ids_list)
pending_uploads: dict[int, PendingResultUpload] = {}


@broker.subscriber(settings.diagnostic_request_queue)
async def handle_diagnostic_request(obj: object) -> None:
    diagnostic_id = _extract_diagnostic_id(obj)
    file_id = _extract_file_id(obj)
    user_id = _extract_user_id(obj)
    if diagnostic_id is None:
        logger.warning("Diagnostic event does not contain diagnostic id: %r", obj)
        return
    if file_id is None:
        logger.warning("Diagnostic event does not contain file_id: %r", obj)
        return
    if user_id is None:
        logger.warning("Diagnostic event does not contain user_id: %r", obj)
        return

    try:
        logger.info(
            "Received diagnostic event with diagnostic_id=%s user_id=%s file_id=%s, notifying %s chats",
            diagnostic_id,
            user_id,
            file_id,
            len(allowed_chat_ids),
        )
        user = await backend_client.get_user(user_id)
        downloaded_file = await backend_client.download_file(file_id)
        notification_text = _build_notification_text(user.username, user_id)
        await telegram_client.broadcast(
            allowed_chat_ids,
            notification_text,
            reply_markup=_build_result_button(diagnostic_id, user_id),
        )
        await telegram_client.broadcast_voice(
            allowed_chat_ids,
            downloaded_file.content,
            downloaded_file.filename,
            downloaded_file.content_type,
        )
    except Exception:
        logger.exception(
            "Failed to process diagnostic event for diagnostic_id=%s user_id=%s file_id=%s",
            diagnostic_id,
            user_id,
            file_id,
        )


async def handle_admin_callback(callback_query: dict[str, Any]) -> None:
    callback_query_id = callback_query.get("id")
    message = callback_query.get("message") or {}
    chat = message.get("chat") or {}
    chat_id = chat.get("id")
    data = callback_query.get("data", "")

    if isinstance(callback_query_id, str):
        await telegram_client.answer_callback_query(callback_query_id)

    if not isinstance(chat_id, int):
        return

    parsed = _parse_result_callback_data(data)
    if parsed is None:
        logger.warning("Unsupported callback payload: %r", data)
        return

    pending_uploads[chat_id] = PendingResultUpload(
        diagnostic_id=parsed.diagnostic_id,
        user_id=parsed.user_id,
    )
    await telegram_client.send_message(chat_id, "Жду файл диагностики для этого пользователя.")


async def handle_admin_message(message: dict[str, Any]) -> None:
    chat = message.get("chat") or {}
    chat_id = chat.get("id")
    if not isinstance(chat_id, int):
        return

    pending_upload = pending_uploads.get(chat_id)
    if pending_upload is None:
        return

    attachment = _extract_attachment(message)
    if attachment is None:
        await telegram_client.send_message(
            chat_id,
            "Ожидаю файл диагностики документом или аудиофайлом.",
        )
        return

    try:
        telegram_file = await telegram_client.download_file(attachment.file_id)
        uploaded_file = await backend_client.upload_file(
            telegram_file.content,
            attachment.filename,
            attachment.content_type,
        )
        diagnostic = await backend_client.get_diagnostic(pending_upload.diagnostic_id)
        await backend_client.patch_diagnostic(
            pending_upload.diagnostic_id,
            {
                "status": DIAGNOSTIC_STATUS_COMPLETED,
                "file_id": diagnostic.file_id,
                "result_file_id": uploaded_file.id,
                "passed_at": datetime.utcnow().isoformat(),
                "user_id": diagnostic.user_id,
            },
        )
        pending_uploads.pop(chat_id, None)
        await telegram_client.send_message(chat_id, "Файл диагностики сохранен.")
    except Exception:
        logger.exception(
            "Failed to save diagnostic result for diagnostic_id=%s user_id=%s",
            pending_upload.diagnostic_id,
            pending_upload.user_id,
        )
        await telegram_client.send_message(
            chat_id,
            "Не удалось сохранить файл диагностики. Попробуйте отправить файл еще раз.",
        )


def _extract_file_id(obj: object) -> int | None:
    if isinstance(obj, dict):
        return _coerce_file_id(obj.get("file_id"))

    if hasattr(obj, "file_id"):
        return _coerce_file_id(getattr(obj, "file_id"))

    return None


def _extract_diagnostic_id(obj: object) -> int | None:
    if isinstance(obj, dict):
        return _coerce_file_id(obj.get("id"))

    if hasattr(obj, "id"):
        return _coerce_file_id(getattr(obj, "id"))

    return None


def _extract_user_id(obj: object) -> int | None:
    if isinstance(obj, dict):
        return _coerce_file_id(obj.get("user_id"))

    if hasattr(obj, "user_id"):
        return _coerce_file_id(getattr(obj, "user_id"))

    return None


def _coerce_file_id(value: Any) -> int | None:
    if isinstance(value, int):
        return value

    if isinstance(value, str) and value.isdigit():
        return int(value)

    return None


def _build_notification_text(username: str | None, user_id: int) -> str:
    display_name = username.strip() if isinstance(username, str) else ""
    if not display_name:
        display_name = f"id={user_id}"

    return f"Пользователь ({display_name}) хочет пройти диагностику"


def _build_result_button(diagnostic_id: int, user_id: int) -> dict[str, Any]:
    return {
        "inline_keyboard": [
            [
                {
                    "text": "Отправить результат",
                    "callback_data": _build_result_callback_data(diagnostic_id, user_id),
                }
            ]
        ]
    }


def _build_result_callback_data(diagnostic_id: int, user_id: int) -> str:
    return f"{RESULT_CALLBACK_PREFIX}:{diagnostic_id}:{user_id}"


def _parse_result_callback_data(data: object) -> PendingResultUpload | None:
    if not isinstance(data, str):
        return None

    prefix, separator, payload = data.partition(":")
    if prefix != RESULT_CALLBACK_PREFIX or not separator:
        return None

    parts = payload.split(":")
    if len(parts) != 2:
        return None

    diagnostic_id = _coerce_file_id(parts[0])
    user_id = _coerce_file_id(parts[1])
    if diagnostic_id is None or user_id is None:
        return None

    return PendingResultUpload(diagnostic_id=diagnostic_id, user_id=user_id)


def _extract_attachment(message: dict[str, Any]) -> TelegramAttachment | None:
    document = message.get("document")
    if isinstance(document, dict):
        file_id = document.get("file_id")
        if isinstance(file_id, str):
            return TelegramAttachment(
                file_id=file_id,
                filename=_coerce_filename(document.get("file_name"), file_id, "result.bin"),
                content_type=_coerce_content_type(
                    document.get("mime_type"),
                    "application/octet-stream",
                ),
            )

    audio = message.get("audio")
    if isinstance(audio, dict):
        file_id = audio.get("file_id")
        if isinstance(file_id, str):
            return TelegramAttachment(
                file_id=file_id,
                filename=_coerce_filename(audio.get("file_name"), file_id, "result_audio.mp3"),
                content_type=_coerce_content_type(audio.get("mime_type"), "audio/mpeg"),
            )

    return None


def _coerce_filename(value: object, file_id: str, fallback: str) -> str:
    if isinstance(value, str) and value.strip():
        return value.strip()

    return fallback if fallback else f"file_{file_id}"


def _coerce_content_type(value: object, fallback: str) -> str:
    if isinstance(value, str) and value.strip():
        return value.strip()

    return fallback


async def run_broker() -> None:
    await broker.start()
    logger.info(
        "RabbitMQ consumer started for queue=%s",
        settings.diagnostic_request_queue,
    )
    try:
        await asyncio.Event().wait()
    finally:
        await broker.close()


async def main() -> None:
    logger.info("Starting admin bot")

    broker_task = asyncio.create_task(run_broker(), name="rabbit-broker")
    polling_task = asyncio.create_task(
        telegram_client.poll_updates(
            allowed_chat_ids,
            on_message=handle_admin_message,
            on_callback_query=handle_admin_callback,
        ),
        name="telegram-polling",
    )

    try:
        done, pending = await asyncio.wait(
            {broker_task, polling_task},
            return_when=asyncio.FIRST_EXCEPTION,
        )

        for task in done:
            exception = task.exception()
            if exception is not None:
                raise exception

        for task in pending:
            task.cancel()
            with suppress(asyncio.CancelledError):
                await task
    finally:
        await backend_client.close()
        await telegram_client.close()


if __name__ == "__main__":
    asyncio.run(main())
