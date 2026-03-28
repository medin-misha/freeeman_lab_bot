import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from config import settings
from core.utils import parse_result_callback_data

from .states import DiagnosticStates


logger = logging.getLogger(__name__)

router = Router(name="diagnostics_callbacks")
router.callback_query.filter(F.message.chat.id.in_(settings.chat_ids_list))

RESULT_CALLBACK_PREFIX = settings.message.text.get("callback", {}).get(
    "send_result",
    "send_result",
)


@router.callback_query()
async def send_result_callback(
    query: CallbackQuery,
    state: FSMContext,
) -> None:
    parsed = parse_result_callback_data(query.data, RESULT_CALLBACK_PREFIX)
    await query.answer()
    if parsed is None:
        logger.warning("Unsupported callback payload: %r", query.data)
        return

    notification_message_id = query.message.message_id if query.message is not None else None
    notification_chat_id = query.message.chat.id if query.message is not None else None

    await state.update_data(
        {
            "diagnostic_id": parsed.diagnostic_id,
            "user_id": parsed.user_id,
            "notification_message_id": notification_message_id,
            "notification_chat_id": notification_chat_id,
        }
    )
    await state.set_state(DiagnosticStates.waiting_for_result_file)

    if query.message is not None:
        await query.message.reply(
            settings.message.text.get("diagnostics", {}).get(
                "wait_for_result_file",
                "Жду файл диагностики для этого пользователя.",
            )
        )
