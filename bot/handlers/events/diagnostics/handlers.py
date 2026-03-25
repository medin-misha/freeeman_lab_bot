from aiogram import F, Router, types
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
from .states import DiagnosticStates
from core.utils.api import DiagnosticsAPI

from config import settings
from .buttons import send_voice_inline_keyboard, confirmation_reply_keyboard
from core.utils import check_sub_channel_dec

router = Router(name="diagnostics_handlers")

@router.message(F.text.lower() == "диагностика")
@check_sub_channel_dec
async def analysis_handler(msg: types.Message):
    await msg.reply(
        text=settings.message.text.get("analysis"),
        reply_markup=send_voice_inline_keyboard(),
    )
    await msg.reply_document(
        document=FSInputFile(path=settings.files.analysis_file_pdf),
    )

@router.message(DiagnosticStates.waiting_for_audio, F.voice)
async def voice_handler(msg: types.Message, state: FSMContext):
    await msg.answer(text="Подтвердить отправку, или попробовать ещё раз?", reply_markup=confirmation_reply_keyboard())
    await state.update_data({"voice": msg.voice})
    await state.set_state(DiagnosticStates.confirmation)

@router.message(DiagnosticStates.confirmation, F.text.lower() == "отправить")
async def confirmation_handler(msg: types.Message, state: FSMContext):
    await msg.answer(text="Спасибо, я получил твое голосовое сообщение. Скоро я его прослушаю и дам обратную связь")
    data = await state.get_data()
    await DiagnosticsAPI().create_diagnostic(voice=data["voice"], chat_id=msg.chat.id, bot=msg.bot)
    await state.clear()

@router.message(DiagnosticStates.confirmation, F.text.lower() == "ещё раз")
async def confirmation_handler(msg: types.Message, state: FSMContext):
    await msg.answer(text="Жду твоё голосовое сообщение")
    await state.set_state(DiagnosticStates.waiting_for_audio)
