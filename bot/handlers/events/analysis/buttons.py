from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


PAID_ANALYSIS_URL = (
    "https://docs.google.com/forms/d/e/1FAIpQLSfrNR-BjZIZO-YFt4K60Nc01ZCRA9X9kgw2Kx7qU1bCBX4K3w/viewform"
)
FREE_ANALYSIS_URL = (
    "https://docs.google.com/forms/d/e/1FAIpQLSeQ0Ubtz3nNgXlxzOcIZ2azImdEwcJz-KBQ74nObMW-2FUzVQ/viewform"
)
SCHEDULE_URL = "https://docs.google.com/spreadsheets/d/1vJppYEgiGRyplpqPmBuXs2LL1rRRpoRQ4K7ej1ro60Q/edit?usp=sharing"
FORM_FILLED_TEXT = "Форму заполнил!"

def analysis_format_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Публичный разбор(бесплатно)",
                    url=FREE_ANALYSIS_URL,
                )
            ],
            [
                InlineKeyboardButton(
                    text="Приватный разбор(платно)",
                    url=PAID_ANALYSIS_URL,
                )
            ],
        ]
    )

def wording_of_request_for_analysis_inline_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Я готов к разбору!")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

def analysis_form_filled_reply_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=FORM_FILLED_TEXT)],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

def schedule_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Расписание", url=SCHEDULE_URL)]
        ]
    )
