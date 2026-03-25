from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def start_reply_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="МАСШТАБ")]]
    )
