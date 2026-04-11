import logging

from aiogram import Bot, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import ErrorEvent, Message

from config import settings
from core.states import FSMError

router = Router(name="errors")
logger = logging.getLogger(__name__)


@router.error()
async def error_handler(event: ErrorEvent, bot: Bot, state: FSMContext) -> None:
    logger.exception("Unhandled error: %s", event.exception, exc_info=event.exception)

    await state.set_state(FSMError.error)
    print(event.exception)
    update = event.update
    chat_id: int | None = None

    if update.message:
        chat_id = update.message.chat.id
    elif update.callback_query and update.callback_query.message:
        chat_id = update.callback_query.message.chat.id

    if chat_id is not None:
        await bot.send_message(
            chat_id=chat_id,
            text=settings.message.text.get("errors").get("non_flow_error"),
        )

@router.message()
async def any_message_handler(msg: Message) -> None:
    await msg.answer(
        text=settings.message.text.get("errors").get("any_massage_text"),
    )