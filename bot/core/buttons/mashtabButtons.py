from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from config import settings

def mashtab_inline() -> InlineKeyboardMarkup:
    button_lines: List[InlineKeyboardButton] = [
        [InlineKeyboardButton(text="🟨Оставить обратную связь🟨", url="https://t.me/alexfreemanlifelab/511"),],
    ]

    markup = InlineKeyboardMarkup(inline_keyboard=button_lines)

    return markup
    
def analysis_reply() -> ReplyKeyboardMarkup:
    button_lines: List[KeyboardButton] = [
        [KeyboardButton(text="РАЗБОР"),],
    ]

    markup = ReplyKeyboardMarkup(keyboard=button_lines)

    return markup   