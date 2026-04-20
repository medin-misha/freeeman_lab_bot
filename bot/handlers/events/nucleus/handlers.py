from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message

from config import settings
from core.utils import ensure_user_registered
from handlers.events.diagnostics.buttons import diagnostic_result_reply_keyboard

from .buttons import (
    nucleus_application_reply_keyboard,
    nucleus_how_to_join_reply_keyboard,
    nucleus_inside_reply_keyboard,
    nucleus_intro_reply_keyboard,
)
from .publisher import publish_nucleus_application
from .states import NucleusStates


router = Router(name="nucleus_handlers")

RETURN_TO_INTRO = "intro"
RETURN_TO_INSIDE = "inside"
INSIDE_BUTTON_TEXTS = ("что будет внутри",)
HOW_TO_JOIN_BUTTON_TEXTS = ("каĸ попасть", "как попасть", "доступ сĸоро отĸроется", "доступ скоро откроется")
APPLICATION_BUTTON_TEXTS = ("оставить заявĸу в «ядро»", "оставить заявку в «ядро»")


async def send_nucleus_intro(msg: Message, state: FSMContext) -> None:
    await state.set_state(NucleusStates.intro)
    await state.update_data({"nucleus_how_to_join_return_to": RETURN_TO_INTRO})
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action="upload_video")
    await msg.answer_video(
        video=FSInputFile(path=settings.files.nucleus_intro_video),
    )
    await msg.answer(
        text=settings.message.text.get("nucleus_intro"),
        reply_markup=nucleus_intro_reply_keyboard(),
    )


async def send_nucleus_inside(msg: Message, state: FSMContext) -> None:
    await state.set_state(NucleusStates.inside)
    await msg.answer(
        text=settings.message.text.get("nucleus_inside"),
        reply_markup=nucleus_inside_reply_keyboard(),
    )


async def send_nucleus_how_to_join(
    msg: Message,
    state: FSMContext,
    return_to: str,
) -> None:
    await state.set_state(NucleusStates.how_to_join)
    await state.update_data({"nucleus_how_to_join_return_to": return_to})
    await msg.answer(
        text=settings.message.text.get("nucleus_how_to_join"),
        reply_markup=nucleus_how_to_join_reply_keyboard(),
    )


async def send_nucleus_application_prompt(
    msg: Message,
    state: FSMContext,
) -> None:
    await state.set_state(NucleusStates.waiting_for_application)
    await msg.answer(
        text=settings.message.text.get("nucleus_application_prompt"),
        reply_markup=nucleus_application_reply_keyboard(),
    )


@router.message(F.text.lower() == "узнать про «ядро»")
@ensure_user_registered
async def nucleus_entry_handler(msg: Message, state: FSMContext) -> None:
    await state.clear()
    await send_nucleus_intro(msg, state)


@router.message(F.text.lower().in_(INSIDE_BUTTON_TEXTS))
@ensure_user_registered
async def nucleus_inside_handler(msg: Message, state: FSMContext) -> None:
    await send_nucleus_inside(msg, state)


@router.message(
    F.text.lower().in_(HOW_TO_JOIN_BUTTON_TEXTS),
)
@ensure_user_registered
async def nucleus_how_to_join_handler(msg: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    return_to = RETURN_TO_INSIDE
    if current_state == NucleusStates.intro.state:
        return_to = RETURN_TO_INTRO

    await send_nucleus_how_to_join(msg, state, return_to)


@router.message(
    F.text.lower().in_(APPLICATION_BUTTON_TEXTS),
)
@ensure_user_registered
async def nucleus_application_prompt_handler(msg: Message, state: FSMContext) -> None:
    await send_nucleus_application_prompt(msg, state)


@router.message(
    StateFilter(
        NucleusStates.intro,
        NucleusStates.inside,
        NucleusStates.how_to_join,
        NucleusStates.waiting_for_application,
    ),
    F.text.lower() == "назад",
)
@ensure_user_registered
async def nucleus_back_handler(msg: Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state == NucleusStates.intro.state:
        await state.clear()
        await msg.answer(
            text="Выбирай следующий шаг.",
            reply_markup=diagnostic_result_reply_keyboard(),
        )
        return

    if current_state == NucleusStates.inside.state:
        await send_nucleus_intro(msg, state)
        return

    if current_state == NucleusStates.how_to_join.state:
        data = await state.get_data()
        if data.get("nucleus_how_to_join_return_to") == RETURN_TO_INSIDE:
            await send_nucleus_inside(msg, state)
            return

        await send_nucleus_intro(msg, state)
        return

    if current_state == NucleusStates.waiting_for_application.state:
        data = await state.get_data()
        return_to = data.get("nucleus_how_to_join_return_to", RETURN_TO_INTRO)
        await send_nucleus_how_to_join(msg, state, return_to)
        return

    await state.clear()
    await msg.answer(
        text="Выбирай следующий шаг.",
        reply_markup=diagnostic_result_reply_keyboard(),
    )


@router.message(NucleusStates.waiting_for_application, F.text)
@ensure_user_registered
async def nucleus_application_handler(msg: Message, state: FSMContext) -> None:
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action="typing")

    from_user = msg.from_user
    if from_user is None:
        username = None
        first_name = None
        last_name = None
    else:
        username = from_user.username
        first_name = from_user.first_name
        last_name = from_user.last_name

    provided_name = _extract_provided_name(msg.text)
    submitted_at = msg.date.astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    await publish_nucleus_application(
        {
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "provided_name": provided_name,
            "application_text": msg.text,
            "submitted_at": submitted_at,
        }
    )

    await state.clear()
    await msg.answer(
        text=settings.message.text.get("nucleus_application_saved"),
        reply_markup=diagnostic_result_reply_keyboard(),
    )


@router.message(NucleusStates.waiting_for_application)
@ensure_user_registered
async def nucleus_application_invalid_handler(msg: Message) -> None:
    await msg.answer(
        text=settings.message.text.get("errors", {}).get(
            "nucleus_waiting_for_application",
            "Сейчас я жду заявку в «Ядро» одним текстовым сообщением.",
        )
    )


def _extract_provided_name(text: str) -> str | None:
    for line in text.splitlines():
        normalized = line.strip()
        if normalized:
            return normalized

    return None
