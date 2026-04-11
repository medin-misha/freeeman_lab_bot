from aiogram import F, Router, types
from aiogram.filters import StateFilter
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
from .states import DiagnosticStates
from core.utils.api import DiagnosticsAPI

from config import settings
from .buttons import (
    confirmation_reply_keyboard,
    save_as_diagnostic_reply_keyboard,
    send_voice_inline_keyboard,
)
from core.utils import check_sub_channel_dec, ensure_user_registered

router = Router(name="diagnostics_handlers")


async def _send_diagnostic(
    msg: types.Message,
    state: FSMContext,
) -> None:
    data = await state.get_data()
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action="typing")
    await DiagnosticsAPI().create_diagnostic(
        telegram_file=data["diagnostic_file"],
        description=data.get("description"),
        chat_id=str(msg.chat.id),
        bot=msg.bot,
        from_user=msg.from_user,
    )
    await state.clear()
    await msg.answer(
        text="Спасибо, я получил твой файл. Скоро я его просмотрю и дам обратную связь",
        reply_markup=types.ReplyKeyboardRemove(),
    )


@router.message(F.text.lower() == "диагностика")
@ensure_user_registered
@check_sub_channel_dec
async def analysis_handler(msg: types.Message):
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action="upload_document")
    await msg.reply(
        text=settings.message.text.get("analysis"),
        reply_markup=send_voice_inline_keyboard(),
    )
    await msg.reply_document(
        document=FSInputFile(path=settings.files.analysis_file_pdf),
    )


@router.message(DiagnosticStates.waiting_for_audio, F.document | F.voice | F.audio)
@ensure_user_registered
async def voice_handler(msg: types.Message, state: FSMContext):
    diagnostic_file = msg.voice or msg.document or msg.audio
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action="typing")
    await msg.answer(
        text=settings.message.text.get(
            "diagnostic_description_prompt",
            "Пришли одним сообщением:\n"
            "ФИО, Возраст, Город\n\n"
            "И по желанию:\n"
            "1. Какой вопрос задел сильнее всего?\n"
            "2. Где было самое большое напряжение?\n"
            "3. Где поднялись самые сильные эмоции?\n"
            "4. Где пришел важный инсайт?\n"
            "5. Какой шаг на 72 часа ты выбрал?",
        ),
    )
    await state.update_data({"diagnostic_file": diagnostic_file})
    await state.set_state(DiagnosticStates.waiting_for_description)


@router.message(DiagnosticStates.waiting_for_description, F.text)
@ensure_user_registered
async def description_handler(msg: types.Message, state: FSMContext):
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action="typing")
    await state.update_data({"description": msg.text})
    await msg.answer(
        text="Подтвердить отправку, или попробовать ещё раз?",
        reply_markup=confirmation_reply_keyboard(),
    )
    await state.set_state(DiagnosticStates.confirmation)


@router.message(DiagnosticStates.waiting_for_description)
@ensure_user_registered
async def description_invalid_handler(msg: types.Message):
    await msg.answer(
        text=settings.message.text.get(
            "diagnostic_description_invalid",
            "Пришли ответ одним текстовым сообщением.",
        )
    )


@router.message(DiagnosticStates.confirmation, F.text.lower() == "отправить")
@ensure_user_registered
async def confirmation_handler(msg: types.Message, state: FSMContext):
    await _send_diagnostic(msg, state)


@router.message(DiagnosticStates.confirmation, F.text.lower() == "ещё раз")
@ensure_user_registered
async def confirmation_retry_handler(msg: types.Message, state: FSMContext):
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action="typing")
    await state.update_data({"diagnostic_file": None, "description": None})
    await msg.answer(text="Жду твоё голосовое сообщение или документ")
    await state.set_state(DiagnosticStates.waiting_for_audio)

@router.message(DiagnosticStates.confirmation, F.text.lower() != "отправить" and F.text.lower() != "ещё раз")
async def confirmation_invalid_handler(msg: types.Message):
    await msg.answer(text="Пожалуйста, используй кнопки", reply_markup=confirmation_reply_keyboard())
