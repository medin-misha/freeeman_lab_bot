import io
import logging
from datetime import datetime

from aiogram import Bot, F, Router, types
from aiogram.fsm.context import FSMContext

from config import settings
from core.utils import DiagnosticsAPI, FileAPI, extract_attachment

from .states import DiagnosticStates


logger = logging.getLogger(__name__)

router = Router(name="diagnostics_handlers")
router.message.filter(F.chat.id.in_(settings.chat_ids_list))

diagnostics_api = DiagnosticsAPI()
file_api = FileAPI()

DIAGNOSTIC_STATUS_COMPLETED = "completed"


@router.message(DiagnosticStates.waiting_for_result_file, F.document | F.audio)
async def save_result_file_handler(
    msg: types.Message,
    state: FSMContext,
    bot: Bot,
) -> None:
    state_data = await state.get_data()
    diagnostic_id = state_data.get("diagnostic_id")
    user_id = state_data.get("user_id")

    if not isinstance(diagnostic_id, int) or not isinstance(user_id, int):
        logger.warning("Invalid diagnostic result state payload: %r", state_data)
        await state.clear()
        await msg.answer(
            settings.message.text.get("diagnostics", {}).get(
                "result_save_error",
                "Не удалось сохранить файл диагностики. Попробуйте отправить файл еще раз.",
            )
        )
        return

    attachment = extract_attachment(msg)
    if attachment is None:
        await msg.answer(
            settings.message.text.get("diagnostics", {}).get(
                "invalid_attachment",
                "Ожидаю файл диагностики документом",
            )
        )
        return

    try:
        telegram_file = await bot.get_file(attachment.file_id)
        buffer = io.BytesIO()
        await bot.download_file(telegram_file.file_path, destination=buffer)
        buffer.seek(0)

        uploaded_file = await file_api.upload_file(
            buffer.getvalue(),
            attachment.filename,
            attachment.content_type,
        )
        diagnostic = await diagnostics_api.get_diagnostic_by_id(diagnostic_id)
        await diagnostics_api.patch_diagnostic(
            diagnostic_id,
            {
                "status": DIAGNOSTIC_STATUS_COMPLETED,
                "file_id": diagnostic.file_id,
                "result_file_id": uploaded_file.id,
                "passed_at": datetime.utcnow().isoformat(),
                "user_id": diagnostic.user_id,
            },
        )
        notification_message_id = state_data.get("notification_message_id")
        notification_chat_id = state_data.get("notification_chat_id")
        await state.clear()
        if notification_message_id is not None and notification_chat_id is not None:
            try:
                await bot.edit_message_reply_markup(
                    chat_id=notification_chat_id,
                    message_id=notification_message_id,
                    reply_markup=None,
                )
            except Exception:
                logger.warning(
                    "Failed to remove inline keyboard from notification message_id=%s chat_id=%s",
                    notification_message_id,
                    notification_chat_id,
                )
        await msg.answer(
            settings.message.text.get("diagnostics", {}).get(
                "result_saved",
                "Файл диагностики сохранен.",
            )
        )
    except Exception:
        logger.exception(
            "Failed to save diagnostic result for diagnostic_id=%s user_id=%s",
            diagnostic_id,
            user_id,
        )
        await msg.answer(
            settings.message.text.get("diagnostics", {}).get(
                "result_save_error",
                "Не удалось сохранить файл диагностики. Попробуйте отправить файл еще раз.",
            )
        )


@router.message(DiagnosticStates.waiting_for_result_file)
async def invalid_attachment_handler(msg: types.Message) -> None:
    await msg.answer(
        settings.message.text.get("diagnostics", {}).get(
            "invalid_attachment",
            "Ожидаю файл диагностики документом",
        )
    )
