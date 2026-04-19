from aiogram import F, Router, types
from aiogram.types import Audio, Document, FSInputFile, Voice
from aiogram.fsm.context import FSMContext

from .states import DiagnosticStates
from .buttons import (
    basic_diagnostic_reply_keyboard,
    diagnostic_menu_reply_keyboard,
    expanded_diagnostic_ready_reply_keyboard,
    expanded_diagnostic_upload_reply_keyboard,
)
from core.utils.api import DiagnosticsAPI

from config import settings
from core.utils import check_sub_channel_dec, ensure_user_registered

router = Router(name="diagnostics_handlers")
MAX_DIAGNOSTIC_FILE_SIZE = 1000 * 1024 * 1024


def _extract_diagnostic_file(
    msg: types.Message,
) -> Audio | Document | Voice | None:
    return msg.voice or msg.audio or msg.document


def validate_diagnostic_file(
    diagnostic_file: Audio | Document | Voice | None,
) -> None:
    from handlers.errors.exceptions import (
        FileTooLargeError,
        InvalidDiagnosticFileError,
    )

    if diagnostic_file is None:
        raise InvalidDiagnosticFileError()

    file_size = getattr(diagnostic_file, "file_size", None)
    if file_size is not None and file_size > MAX_DIAGNOSTIC_FILE_SIZE:
        raise FileTooLargeError()


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
        text=settings.message.text.get("expanded_diagnostic_received"),
        reply_markup=types.ReplyKeyboardRemove(),
    )


async def _send_diagnostic_menu(msg: types.Message, state: FSMContext) -> None:
    await state.clear()
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action="upload_video")
    await msg.answer_video(
        video=FSInputFile(path=settings.files.expanded_diagnostic_video),
    )
    await msg.answer(
        text=settings.message.text.get("expanded_diagnostic_intro"),
        reply_markup=diagnostic_menu_reply_keyboard(),
    )


@router.message(F.text.lower() == "пройти диагностиĸу")
@ensure_user_registered
@check_sub_channel_dec
async def diagnostic_menu_handler(msg: types.Message, state: FSMContext):
    await _send_diagnostic_menu(msg, state)


@router.message(F.text.lower() == "базовая диагностиĸа")
@ensure_user_registered
@check_sub_channel_dec
async def basic_diagnostic_handler(msg: types.Message, state: FSMContext):
    await state.clear()
    await msg.answer(
        text=settings.message.text.get("basic_diagnostic_intro"),
        reply_markup=basic_diagnostic_reply_keyboard(),
    )


@router.message(F.text.lower() == "зачем мне диагностиĸа")
@ensure_user_registered
@check_sub_channel_dec
async def why_diagnostic_handler(msg: types.Message, state: FSMContext):
    await state.clear()
    await msg.answer(
        text=settings.message.text.get("why_diagnostic_intro"),
        reply_markup=basic_diagnostic_reply_keyboard(),
    )


@router.message(F.text.lower() == "назад ĸ диагностиĸе")
@ensure_user_registered
@check_sub_channel_dec
async def back_to_diagnostic_handler(msg: types.Message, state: FSMContext):
    await _send_diagnostic_menu(msg, state)


@router.message(F.text.lower() == "пройти расширенную диагностиĸу")
@ensure_user_registered
@check_sub_channel_dec
async def expanded_diagnostic_start_handler(msg: types.Message, state: FSMContext):
    await state.clear()
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action="upload_video")
    await msg.answer_video(
        video=FSInputFile(path=settings.files.expanded_diagnostic_intro_video),
    )
    await msg.answer_document(
        document=FSInputFile(path=settings.files.analysis_file_pdf),
    )
    await msg.answer(
        text=settings.message.text.get("expanded_diagnostic_start"),
        reply_markup=expanded_diagnostic_ready_reply_keyboard(),
    )


@router.message(F.text.lower() == "я готов(а), отправляю аудио")
@ensure_user_registered
@check_sub_channel_dec
async def analysis_handler(msg: types.Message, state: FSMContext):
    await state.clear()
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action="typing")
    await msg.answer(
        text=settings.message.text.get("expanded_diagnostic_upload_prompt"),
        reply_markup=expanded_diagnostic_upload_reply_keyboard(),
    )
    await state.set_state(DiagnosticStates.waiting_for_audio)

@router.message(F.document | F.voice | F.audio)
@ensure_user_registered
async def diagnostic_file_handler(msg: types.Message, state: FSMContext):
    diagnostic_file = _extract_diagnostic_file(msg)
    validate_diagnostic_file(diagnostic_file)
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


@router.message(DiagnosticStates.waiting_for_audio)
@ensure_user_registered
async def waiting_for_file_invalid_handler(msg: types.Message):
    await msg.answer(
        text=settings.message.text.get("errors", {}).get(
            "diagnostic_waiting_for_file",
            (
                "Сейчас я жду файл диагностики: голосовое, аудио или документ "
                "до 1000 МБ."
            ),
        )
    )


@router.message(DiagnosticStates.waiting_for_description, F.text)
@ensure_user_registered
async def description_handler(msg: types.Message, state: FSMContext):
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action="typing")
    await state.update_data({"description": msg.text})
    await _send_diagnostic(msg, state)


@router.message(DiagnosticStates.waiting_for_description, F.document | F.voice | F.audio)
@ensure_user_registered
async def description_new_file_handler(msg: types.Message, state: FSMContext):
    diagnostic_file = _extract_diagnostic_file(msg)
    validate_diagnostic_file(diagnostic_file)
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
    from handlers.errors.exceptions import InvalidDiagnosticDescriptionError

    raise InvalidDiagnosticDescriptionError()
