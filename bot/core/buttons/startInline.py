from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import settings

def start_inline() -> InlineKeyboardMarkup:
    button_lines: List[InlineKeyboardButton] = [
        [InlineKeyboardButton(text="Вступить", url="https://t.me/alexfreemanlifelab"),],
        [
            InlineKeyboardButton(
                text="🟩Уже вступил🟩",
                callback_data=settings.message.text.get("callback").get("check_subscribe")
            ),
        ],
    ]

    markup = InlineKeyboardMarkup(inline_keyboard=button_lines)

    return markup
    
