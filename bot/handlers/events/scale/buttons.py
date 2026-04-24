from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def scale_reply_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Пройти диагностиĸу")],
            [KeyboardButton(text="Ядро")],
            [KeyboardButton(text="Еще возможности")],
            [KeyboardButton(text="Назад в меню")],
        ],
    )
