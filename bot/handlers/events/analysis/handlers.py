from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from config import settings

from .buttons import (
    analysis_back_reply_keyboard,
    analysis_entry_inline_keyboard,
    analysis_format_inline_keyboard,
    analysis_schedule_inline_keyboard,
)
from .states import AnalysisStates
from core.utils import ensure_user_registered
from handlers.events.diagnostics.buttons import diagnostic_result_reply_keyboard

router = Router(name="analysis_handlers")


async def send_analysis_entry(
    msg: Message,
    state: FSMContext,
) -> None:
    await state.set_state(AnalysisStates.choosing_format)
    await msg.answer(
        text=settings.message.text.get("analysis_intro"),
        reply_markup=analysis_entry_inline_keyboard(),
    )


async def send_analysis_format_intro(
    msg: Message,
    state: FSMContext,
    format_name: str,
) -> None:
    if format_name == "public":
        await state.set_state(AnalysisStates.public_intro)
        text = settings.message.text.get("analysis_public_intro")
    else:
        await state.set_state(AnalysisStates.private_intro)
        text = settings.message.text.get("analysis_private_intro")

    await msg.answer(
        text=text,
        reply_markup=analysis_format_inline_keyboard(format_name),
    )
    await msg.answer(
        text=settings.message.text.get("analysis_back_hint"),
        reply_markup=analysis_back_reply_keyboard(),
    )


async def send_analysis_schedule_intro(
    msg: Message,
    state: FSMContext,
    format_name: str,
) -> None:
    if format_name == "public":
        await state.set_state(AnalysisStates.public_schedule)
    else:
        await state.set_state(AnalysisStates.private_schedule)

    await msg.answer(
        text=settings.message.text.get("analysis_schedule_intro"),
        reply_markup=analysis_schedule_inline_keyboard(format_name),
    )
    await msg.answer(
        text=settings.message.text.get("analysis_back_hint"),
        reply_markup=analysis_back_reply_keyboard(),
    )


@router.message(F.text.lower().in_(("пойти в разбор", "разбор")))
@ensure_user_registered
async def analysis_entry_handler(msg: Message, state: FSMContext) -> None:
    await state.clear()
    await send_analysis_entry(msg, state)


@router.message(
    StateFilter(
        AnalysisStates.choosing_format,
        AnalysisStates.public_intro,
        AnalysisStates.private_intro,
        AnalysisStates.public_schedule,
        AnalysisStates.private_schedule,
    ),
    F.text.lower() == "назад",
)
@ensure_user_registered
async def analysis_back_handler(msg: Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state == AnalysisStates.choosing_format.state:
        await state.clear()
        await msg.answer(
            text="Выбирай следующий шаг.",
            reply_markup=diagnostic_result_reply_keyboard(),
        )
        return

    if current_state in {
        AnalysisStates.public_intro.state,
        AnalysisStates.private_intro.state,
    }:
        await send_analysis_entry(msg, state)
        return

    if current_state == AnalysisStates.public_schedule.state:
        await send_analysis_format_intro(msg, state, "public")
        return

    if current_state == AnalysisStates.private_schedule.state:
        await send_analysis_format_intro(msg, state, "private")
        return

    await state.clear()
    await msg.answer(
        text="Выбирай следующий шаг.",
        reply_markup=diagnostic_result_reply_keyboard(),
    )
