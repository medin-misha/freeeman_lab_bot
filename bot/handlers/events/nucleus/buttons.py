from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from config import settings


def nucleus_mini_app_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Узнать про ядро",
                    web_app=WebAppInfo(url=settings.core_min_app),
                )
            ]
        ]
    )
