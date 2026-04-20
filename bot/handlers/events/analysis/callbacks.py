import logging
from datetime import datetime, timezone

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from config import settings
from handlers.events.diagnostics.buttons import diagnostic_result_reply_keyboard
from .publisher import publish_analysis_schedule_confirmation
from .handlers import (
    send_analysis_format_intro,
    send_analysis_schedule_intro,
)


router = Router(name="analysis_callbacks")
logger = logging.getLogger(__name__)


async def _publish_analysis_schedule_confirmation(
    format_name: str,
) -> None:
    confirmed_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    await publish_analysis_schedule_confirmation(
        {
            "analysis_format": format_name,
            "confirmed_at": confirmed_at,
        }
    )


@router.callback_query(
    F.data == settings.message.text.get("callback", {}).get("analysis_back")
)
async def analysis_back_callback(
    query: CallbackQuery,
    state: FSMContext,
) -> None:
    await query.answer()
    if query.message is None:
        return

    await state.clear()
    await query.message.answer(
        text="Выбирай следующий шаг.",
        reply_markup=diagnostic_result_reply_keyboard(),
    )


@router.callback_query(
    F.data == settings.message.text.get("callback", {}).get("analysis_public")
)
async def analysis_public_callback(
    query: CallbackQuery,
    state: FSMContext,
) -> None:
    await query.answer()
    if query.message is None:
        return

    await send_analysis_format_intro(query.message, state, "public")


@router.callback_query(
    F.data == settings.message.text.get("callback", {}).get("analysis_private")
)
async def analysis_private_callback(
    query: CallbackQuery,
    state: FSMContext,
) -> None:
    await query.answer()
    if query.message is None:
        return

    await send_analysis_format_intro(query.message, state, "private")


@router.callback_query(
    F.data
    == settings.message.text.get("callback", {}).get("analysis_public_form_filled")
)
async def analysis_public_form_filled_callback(
    query: CallbackQuery,
    state: FSMContext,
) -> None:
    await query.answer()
    if query.message is None:
        return

    await send_analysis_schedule_intro(query.message, state, "public")


@router.callback_query(
    F.data
    == settings.message.text.get("callback", {}).get("analysis_private_form_filled")
)
async def analysis_private_form_filled_callback(
    query: CallbackQuery,
    state: FSMContext,
) -> None:
    await query.answer()
    if query.message is None:
        return

    await send_analysis_schedule_intro(query.message, state, "private")


@router.callback_query(
    F.data
    == settings.message.text.get("callback", {}).get(
        "analysis_public_schedule_confirmed"
    )
)
async def analysis_public_schedule_confirmed_callback(
    query: CallbackQuery,
    state: FSMContext,
) -> None:
    await query.answer()
    if query.message is None:
        return

    try:
        await _publish_analysis_schedule_confirmation("public")
    except Exception:
        logger.exception("Failed to publish public analysis schedule confirmation")

    await state.clear()
    await query.message.answer(
        text=settings.message.text.get("analysis_schedule_saved"),
        reply_markup=diagnostic_result_reply_keyboard(),
    )


@router.callback_query(
    F.data
    == settings.message.text.get("callback", {}).get(
        "analysis_private_schedule_confirmed"
    )
)
async def analysis_private_schedule_confirmed_callback(
    query: CallbackQuery,
    state: FSMContext,
) -> None:
    await query.answer()
    if query.message is None:
        return

    try:
        await _publish_analysis_schedule_confirmation("private")
    except Exception:
        logger.exception("Failed to publish private analysis schedule confirmation")

    await state.clear()
    await query.message.answer(
        text=settings.message.text.get("analysis_schedule_saved"),
        reply_markup=diagnostic_result_reply_keyboard(),
    )
