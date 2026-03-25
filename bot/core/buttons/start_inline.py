from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import settings


def start_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Вступить",
                    url="https://t.me/alexfreemanlifelab",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🟩Уже вступил🟩",
                    callback_data=settings.message.text.get("callback").get(
                        "check_subscribe"
                    ),
                )
            ],
        ]
    )
