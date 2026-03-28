from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import settings
from core.utils import build_result_callback_data


def send_result_inline_keyboard(
    diagnostic_id: int,
    user_id: int,
) -> InlineKeyboardMarkup:
    callback_prefix = settings.message.text.get("callback", {}).get(
        "send_result",
        "send_result",
    )
    button_text = settings.message.text.get("buttons", {}).get(
        "send_result",
        "Отправить результат",
    )

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=button_text,
                    callback_data=build_result_callback_data(
                        callback_prefix,
                        diagnostic_id,
                        user_id,
                    ),
                )
            ]
        ]
    )
