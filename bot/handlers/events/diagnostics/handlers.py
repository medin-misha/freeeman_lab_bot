from aiogram import F, Router, types
from aiogram.filters import StateFilter
from aiogram.types import Audio, Document, FSInputFile, Voice
from aiogram.fsm.context import FSMContext

from .states import DiagnosticStates
from .buttons import (
    basic_diagnostic_reply_keyboard,
    diagnostic_type_selection_reply_keyboard,
    diagnostic_menu_reply_keyboard,
    diagnostic_sent_reply_keyboard,
    expanded_diagnostic_ready_reply_keyboard,
    expanded_diagnostic_unavailable_reply_keyboard,
    expanded_diagnostic_upload_reply_keyboard,
)
from core.utils.api import DiagnosticsAPI

from config import settings
from core.utils import check_sub_channel_dec, ensure_user_registered

router = Router(name="diagnostics_handlers")
MAX_DIAGNOSTIC_FILE_SIZE = 1000 * 1024 * 1024
BASIC_DIAGNOSTIC_TAG = "#базовая_диагностика"
EXPANDED_DIAGNOSTIC_TAG = "#расширенная_диагностика"
INVISIBILITY_DIAGNOSTIC_TAG = "#диагностика_невидимости"


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


def _append_description_tag(description: str | None, tag: str | None) -> str | None:
    if not tag:
        return description

    normalized_description = (description or "").strip()
    if tag in normalized_description.split():
        return normalized_description or description

    if not normalized_description:
        return tag

    return f"{normalized_description}\n{tag}"


def _normalize_description(description: str | None) -> str | None:
    if not isinstance(description, str):
        return None

    normalized_description = description.strip()
    return normalized_description or None


async def _ask_for_diagnostic_description(msg: types.Message, state: FSMContext) -> None:
    await msg.answer(
        text=settings.message.text.get("diagnostic_getters").get(
            "get_data_for_diagnostic_prompt"
        ),
        reply_markup=expanded_diagnostic_upload_reply_keyboard(),
    )
    await state.set_state(DiagnosticStates.waiting_for_description)


async def _ask_for_diagnostic_type(msg: types.Message, state: FSMContext) -> None:
    await msg.answer(
        text=settings.message.text.get("diagnostic_type_selection_prompt"),
        reply_markup=diagnostic_type_selection_reply_keyboard(),
    )
    await state.set_state(DiagnosticStates.waiting_for_diagnostic_type)


async def _continue_after_diagnostic_type_selected(
    msg: types.Message,
    state: FSMContext,
    diagnostic_tag: str,
) -> None:
    await state.update_data({"diagnostic_tag": diagnostic_tag})
    data = await state.get_data()
    if _normalize_description(data.get("description")) is not None:
        await _send_diagnostic(msg, state)
        return

    await _ask_for_diagnostic_description(msg, state)


async def _store_uploaded_diagnostic(
    msg: types.Message,
    state: FSMContext,
    diagnostic_file: Audio | Document | Voice,
) -> None:
    await state.update_data(
        {
            "diagnostic_file": diagnostic_file,
            "description": _normalize_description(msg.caption),
        }
    )


async def _send_diagnostic(
    msg: types.Message,
    state: FSMContext,
) -> None:
    data = await state.get_data()
    description = _append_description_tag(
        description=data.get("description"),
        tag=data.get("diagnostic_tag"),
    )
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action="typing")
    await DiagnosticsAPI().create_diagnostic(
        telegram_file=data["diagnostic_file"],
        description=description,
        chat_id=str(msg.chat.id),
        bot=msg.bot,
        from_user=msg.from_user,
    )
    await state.clear()
    await msg.answer(
        text=settings.message.text.get("expanded_diagnostic_received"),
        reply_markup=diagnostic_sent_reply_keyboard(),
    )


async def _send_diagnostic_menu(msg: types.Message, state: FSMContext) -> None:
    await state.clear()
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action="upload_video")
    await msg.answer_video(
        video=FSInputFile(path=settings.files.expanded_diagnostic_video),
        width=1080,
        height=1920,
    )
    await msg.answer(
        text=settings.message.text.get("expanded_diagnostic_intro"),
        reply_markup=diagnostic_menu_reply_keyboard(),
    )


async def _start_tagged_diagnostic(
    msg: types.Message,
    state: FSMContext,
    diagnostic_tag: str,
    instruction_path: str,
    include_intro_video: bool = True,
    start_message_key: str = "expanded_diagnostic_start",
) -> None:
    await state.clear()
    await state.update_data({"diagnostic_tag": diagnostic_tag})
    if include_intro_video:
        await msg.bot.send_chat_action(chat_id=msg.chat.id, action="upload_video")
        await msg.answer_video(
            video=FSInputFile(path=settings.files.expanded_diagnostic_intro_video),
            width=1080,
            height=1920,
        )
    await msg.answer_document(
        document=FSInputFile(path=instruction_path),
    )
    await msg.answer(
        text=settings.message.text.get(start_message_key),
        reply_markup=expanded_diagnostic_ready_reply_keyboard(),
    )


@router.message(
    StateFilter(DiagnosticStates.waiting_for_diagnostic_type),
    F.text.lower() == "базовая диагностика",
)
@router.message(
    StateFilter(DiagnosticStates.waiting_for_diagnostic_type),
    F.text.lower() == "базовая диагностиĸа",
)
@ensure_user_registered
@check_sub_channel_dec
async def basic_diagnostic_type_selected_handler(
    msg: types.Message,
    state: FSMContext,
):
    await _continue_after_diagnostic_type_selected(
        msg=msg,
        state=state,
        diagnostic_tag=BASIC_DIAGNOSTIC_TAG,
    )


@router.message(
    StateFilter(DiagnosticStates.waiting_for_diagnostic_type),
    F.text.lower() == "расширенная диагностика",
)
@ensure_user_registered
@check_sub_channel_dec
async def expanded_diagnostic_type_selected_handler(
    msg: types.Message,
    state: FSMContext,
):
    await msg.answer(
        text=settings.message.text.get("expanded_diagnostic_unavailable"),
        reply_markup=expanded_diagnostic_unavailable_reply_keyboard(),
    )


@router.message(
    StateFilter(DiagnosticStates.waiting_for_diagnostic_type),
    F.text.lower() == "диагностика невидимости",
)
@ensure_user_registered
@check_sub_channel_dec
async def invisibility_diagnostic_type_selected_handler(
    msg: types.Message,
    state: FSMContext,
):
    await _continue_after_diagnostic_type_selected(
        msg=msg,
        state=state,
        diagnostic_tag=INVISIBILITY_DIAGNOSTIC_TAG,
    )


@router.message(F.text.lower() == "пройти диагностиĸу")
@ensure_user_registered
@check_sub_channel_dec
async def diagnostic_menu_handler(msg: types.Message, state: FSMContext):
    await _send_diagnostic_menu(msg, state)


@router.message(F.text.lower() == "базовая диагностика")
@router.message(F.text.lower() == "базовая диагностиĸа")
@ensure_user_registered
@check_sub_channel_dec
async def basic_diagnostic_handler(msg: types.Message, state: FSMContext):
    await _start_tagged_diagnostic(
        msg=msg,
        state=state,
        diagnostic_tag=BASIC_DIAGNOSTIC_TAG,
        instruction_path=settings.files.basic_diagnostic_file_pdf,
        include_intro_video=False,
        start_message_key="basic_diagnostic_start",
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


@router.message(F.text.lower() == "расширенная диагностика")
@ensure_user_registered
@check_sub_channel_dec
async def expanded_diagnostic_start_handler(msg: types.Message, state: FSMContext):
    await state.clear()
    await msg.answer(
        text=settings.message.text.get("expanded_diagnostic_unavailable"),
        reply_markup=expanded_diagnostic_unavailable_reply_keyboard(),
    )


@router.message(F.text.lower() == "диагностика невидимости")
@ensure_user_registered
@check_sub_channel_dec
async def invisibility_diagnostic_start_handler(msg: types.Message, state: FSMContext):
    await _start_tagged_diagnostic(
        msg=msg,
        state=state,
        diagnostic_tag=INVISIBILITY_DIAGNOSTIC_TAG,
        instruction_path=settings.files.invisibility_diagnostic_file_pdf,
        include_intro_video=False,
    )


@router.message(F.text.lower() == "я готов(а), отправляю аудио")
@ensure_user_registered
@check_sub_channel_dec
async def analysis_handler(msg: types.Message, state: FSMContext):
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action="typing")
    await msg.answer(
        text=settings.message.text.get("expanded_diagnostic_upload_prompt"),
        reply_markup=expanded_diagnostic_upload_reply_keyboard(),
    )
    await state.set_state(DiagnosticStates.waiting_for_audio)


@router.message(
    StateFilter(
        None,
        DiagnosticStates.waiting_for_audio,
        DiagnosticStates.waiting_for_diagnostic_type,
        DiagnosticStates.waiting_for_description,
    ),
    F.document | F.voice | F.audio,
)
@ensure_user_registered
async def diagnostic_file_handler(msg: types.Message, state: FSMContext):
    diagnostic_file = _extract_diagnostic_file(msg)
    validate_diagnostic_file(diagnostic_file)
    current_state = await state.get_state()

    if current_state == DiagnosticStates.waiting_for_description.state:
        await state.update_data(
            {
                "diagnostic_file": diagnostic_file,
                "description": None,
            }
        )
        await msg.answer(
            text=settings.message.text.get("errors", {}).get(
                "diagnostic_file_replaced",
                "Файл заменён. Теперь пришли описание одним текстовым сообщением.",
            )
        )
        return

    await _store_uploaded_diagnostic(msg, state, diagnostic_file)
    await msg.bot.send_chat_action(chat_id=msg.chat.id, action="typing")
    if current_state == DiagnosticStates.waiting_for_audio.state:
        if _normalize_description(msg.caption) is None:
            await _ask_for_diagnostic_description(msg, state)
            return
        await _send_diagnostic(msg, state)
        return

    await _ask_for_diagnostic_type(msg, state)


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


@router.message(DiagnosticStates.waiting_for_diagnostic_type)
@ensure_user_registered
async def diagnostic_type_invalid_handler(msg: types.Message):
    await msg.answer(
        text=settings.message.text.get("diagnostic_type_selection_invalid"),
        reply_markup=diagnostic_type_selection_reply_keyboard(),
    )


@router.message(DiagnosticStates.waiting_for_description)
@ensure_user_registered
async def description_invalid_handler(msg: types.Message):
    from handlers.errors.exceptions import InvalidDiagnosticDescriptionError

    raise InvalidDiagnosticDescriptionError()
