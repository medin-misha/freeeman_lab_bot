from typing import List

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from config import settings

def start_callback_reply() -> ReplyKeyboardMarkup:
    button_lines: List[KeyboardButton] = [
        [KeyboardButton(text="МАСШТАБ"),],
    ]

    markup = ReplyKeyboardMarkup(keyboard=button_lines)

    return markup
    
