from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


PAID_ANALYSIS_URL = (
    "https://docs.google.com/forms/d/e/1FAIpQLSfrNR-BjZIZO-YFt4K60Nc01ZCRA9X9kgw2Kx7qU1bCBX4K3w/viewform"
)
FREE_ANALYSIS_URL = (
    "https://docs.google.com/forms/d/e/1FAIpQLSeQ0Ubtz3nNgXlxzOcIZ2azImdEwcJz-KBQ74nObMW-2FUzVQ/viewform"
)


def analysis_format_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Бесплатный разбор",
                    url=FREE_ANALYSIS_URL,
                )
            ],
            [
                InlineKeyboardButton(
                    text="Платный разбор",
                    url=PAID_ANALYSIS_URL,
                )
            ],
        ]
    )

def wording_of_request_for_analysis_inline_keyboard() -> InlineKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Я готов к разбору!")],
        ],
    )
    