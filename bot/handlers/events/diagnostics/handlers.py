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
async def analysis_handler(msg: types.Message, state: FSMContext):
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action="upload_document")
    await msg.answer(text=settings.message.text.get("diagnostic"))
    await msg.reply_document(
        document=FSInputFile(path=settings.files.analysis_file_pdf),
        caption=settings.message.text
        .get("diagnostic_getters").get("read_diagnostic_file")
        + "\n" + settings.message.text
        .get("diagnostic_getters").get("get_data_for_diagnostic_prompt"),
    )
    await state.set_state(DiagnosticStates.waiting_for_audio)

    

@router.message(F.document | F.voice | F.audio)
@ensure_user_registered
async def voice_handler(msg: types.Message, state: FSMContext):
    diagnostic_file = msg.voice or msg.document or msg.audio
    await state.update_data({"diagnostic_file": diagnostic_file})
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action="typing")
    if msg.caption is None:
        await msg.answer(
            text=settings.message.text
            .get("diagnostic_getters")
            .get("get_data_for_diagnostic_prompt"),
        )
        await state.set_state(DiagnosticStates.waiting_for_description)
    else:
         await state.update_data({"description": msg.caption})
         await _send_diagnostic(msg, state)


@router.message(DiagnosticStates.waiting_for_description, F.text)
@ensure_user_registered
async def description_handler(msg: types.Message, state: FSMContext):
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action="typing")
    await state.update_data({"description": msg.text})
    await _send_diagnostic(msg, state)
    await state.set_state(DiagnosticStates.confirmation)


@router.message(DiagnosticStates.waiting_for_description, F.document | F.voice | F.audio)
@ensure_user_registered
async def description_new_file_handler(msg: types.Message, state: FSMContext):
    diagnostic_file = msg.voice or msg.document or msg.audio
    await state.update_data({"diagnostic_file": diagnostic_file})
    await msg.answer(
        text=settings.message.text.get("errors", {}).get(
            "diagnostic_file_replaced",
            "Файл заменён. Теперь пришли описание одним текстовым сообщением.",
        )
    )


@router.message(DiagnosticStates.waiting_for_description)
@ensure_user_registered
async def description_invalid_handler(msg: types.Message):
    await msg.answer(
        text=settings.message.text.get(
            "diagnostic_description_invalid",
            "Пришли ответ одним текстовым сообщением.",
        )
    )
