from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from config import settings

def send_voice_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Хочу скинуть голосовое",
                    callback_data=settings.message.text.get("callback").get("send_file"),
                )
            ]
        ]
    )

def confirmation_reply_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Отправить"),
                KeyboardButton(text="Ещё раз")
            ]
        ],
        one_time_keyboard=True
    )

def diagnostic_success_reply_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="РАЗБОР")
            ]
        ],
        one_time_keyboard=True
    )