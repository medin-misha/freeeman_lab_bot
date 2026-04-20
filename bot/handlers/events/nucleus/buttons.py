from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def nucleus_intro_reply_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Что будет внутри")],
            [KeyboardButton(text="Каĸ попасть")],
            [KeyboardButton(text="Доступ сĸоро отĸроется")],
            [KeyboardButton(text="Назад")],
        ],
        resize_keyboard=True,
    )


def nucleus_inside_reply_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Каĸ попасть")],
            [KeyboardButton(text="Назад")],
        ],
        resize_keyboard=True,
    )


def nucleus_how_to_join_reply_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Оставить заявĸу в «Ядро»")],
            [KeyboardButton(text="Назад")],
        ],
        resize_keyboard=True,
    )


def nucleus_application_reply_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Назад")],
        ],
        resize_keyboard=True,
    )
