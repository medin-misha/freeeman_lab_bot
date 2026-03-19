from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

def mashtab_inline() -> InlineKeyboardMarkup:
    button_lines: List[InlineKeyboardButton] = [
        [InlineKeyboardButton(text="🟨Оставить обратную связь🟨", url="https://t.me/alexfreemanlifelab/511"),],
    ]

    markup = InlineKeyboardMarkup(inline_keyboard=button_lines)

    return markup
    
def analysis_reply() -> ReplyKeyboardMarkup:
    button_lines: List[KeyboardButton] = [
        [KeyboardButton(text="ДИАГНОСТИКА"),],
    ]

    markup = ReplyKeyboardMarkup(keyboard=button_lines)

    return markup   

def analysis_inline() -> InlineKeyboardMarkup:
    button_lines: List[InlineKeyboardButton] = [
        [InlineKeyboardButton(text="Аудиофайл скидывать сюда", url="https://forms.yandex.ru/u/69bb9b0ed046881ea28f2497/")],
    ]

    markup = InlineKeyboardMarkup(inline_keyboard=button_lines)

    return markup

def analysis2_reply() -> ReplyKeyboardMarkup:
    button_lines: List[KeyboardButton] = [
        [
            KeyboardButton(text="РАЗБОР"),
        ]
    ]
    markup = ReplyKeyboardMarkup(keyboard=button_lines)

    return markup


def handling_inline() -> InlineKeyboardMarkup:
    button_lines: List[List[InlineKeyboardButton]] = [
        [InlineKeyboardButton(text="🟨ОТЗЫВЫ🟨", url="https://t.me/+tB1WBUwmP-FkOWIy")],
        [
            InlineKeyboardButton(text="Платный разбор", url="https://forms.yandex.ru/u/69bb9d98eb614613534db266"),
            InlineKeyboardButton(text="Бесплатный разбор", url="https://forms.yandex.ru/u/69bb9ca190fa7b1d23215444")
        ],
    ]

    markup = InlineKeyboardMarkup(inline_keyboard=button_lines)

    return markup


def handling_reply() -> ReplyKeyboardMarkup:
    button_lines: List[List[KeyboardButton]] = [
        [KeyboardButton(text="ПЛАТНЫЙ РАЗБОР")],
        [KeyboardButton(text="БЕСПЛАТНЫЙ РАЗБОР")],
    ]

    markup = ReplyKeyboardMarkup(keyboard=button_lines)

    return markup

