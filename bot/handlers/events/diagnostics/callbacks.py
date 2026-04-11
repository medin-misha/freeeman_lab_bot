from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from config import settings
from .states import DiagnosticStates
from core.utils import ensure_user_registered

router = Router(name="diagnostics_callbacks")

# @router.callback_query(F.data == settings.message.text.get("callback").get("send_file"),)
@ensure_user_registered
async def send_file_callback(query: CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(DiagnosticStates.waiting_for_audio)
    await query.answer(text="Отправь голосовое сообщение или документ")
    await query.message.reply(text="Отправь голосовое сообщение или документ")
