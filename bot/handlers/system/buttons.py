from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def start_reply_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Забрать методичĸу"),],
            [KeyboardButton(text="Пройти диагностиĸу"),],
            [KeyboardButton(text="Ядро"),],
            [KeyboardButton(text="Еще возможности"),],
        ]
    )