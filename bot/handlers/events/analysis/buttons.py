from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from config import settings

PAID_ANALYSIS_URL = (
    "https://docs.google.com/forms/d/e/1FAIpQLSfrNR-BjZIZO-YFt4K60Nc01ZCRA9X9kgw2Kx7qU1bCBX4K3w/viewform"
)
FREE_ANALYSIS_URL = (
    "https://docs.google.com/forms/d/e/1FAIpQLSeQ0Ubtz3nNgXlxzOcIZ2azImdEwcJz-KBQ74nObMW-2FUzVQ/viewform"
)
SCHEDULE_URL = "https://docs.google.com/spreadsheets/d/1vJppYEgiGRyplpqPmBuXs2LL1rRRpoRQ4K7ej1ro60Q/edit?usp=sharing"


def analysis_entry_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Публичный разбор",
                    callback_data=settings.message.text.get("callback", {}).get(
                        "analysis_public",
                        "analysis_public",
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    text="Приватный разбор",
                    callback_data=settings.message.text.get("callback", {}).get(
                        "analysis_private",
                        "analysis_private",
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    text="Назад",
                    callback_data=settings.message.text.get("callback", {}).get(
                        "analysis_back",
                        "analysis_back",
                    ),
                )
            ],
        ]
    )


def analysis_back_reply_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Назад")]],
        resize_keyboard=True,
        one_time_keyboard=False,
    )


def analysis_format_inline_keyboard(format_name: str) -> InlineKeyboardMarkup:
    if format_name == "public":
        form_url = FREE_ANALYSIS_URL
        form_filled_callback = settings.message.text.get("callback", {}).get(
            "analysis_public_form_filled",
            "analysis_public_form_filled",
        )
    else:
        form_url = PAID_ANALYSIS_URL
        form_filled_callback = settings.message.text.get("callback", {}).get(
            "analysis_private_form_filled",
            "analysis_private_form_filled",
        )

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Открыть анĸету", url=form_url)],
            [
                InlineKeyboardButton(
                    text="Форму заполнил(а)",
                    callback_data=form_filled_callback,
                )
            ],
        ]
    )


def analysis_schedule_inline_keyboard(format_name: str) -> InlineKeyboardMarkup:
    if format_name == "public":
        schedule_confirmed_callback = settings.message.text.get("callback", {}).get(
            "analysis_public_schedule_confirmed",
            "analysis_public_schedule_confirmed",
        )
    else:
        schedule_confirmed_callback = settings.message.text.get("callback", {}).get(
            "analysis_private_schedule_confirmed",
            "analysis_private_schedule_confirmed",
        )

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Открыть расписание", url=SCHEDULE_URL)],
            [
                InlineKeyboardButton(
                    text="Я внес(ла) себя в расписание",
                    callback_data=schedule_confirmed_callback,
                )
            ],
        ]
    )
