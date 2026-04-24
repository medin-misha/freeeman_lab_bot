from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from config import settings


def send_voice_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Хочу скинуть голосовое или документ",
                    callback_data=settings.message.text.get("callback").get("send_file"),
                )
            ]
        ]
    )


def diagnostic_group_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Добавляйся в группу",
                    url="https://t.me/+tB1WBUwmP-FkOWIy",
                )
            ]
        ]
    )



def save_as_diagnostic_reply_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Да"),
                KeyboardButton(text="Нет")
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


def diagnostic_result_reply_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Пойти в разбор")
            ],
            [
                KeyboardButton(text="Ядро")
            ],
            [
                KeyboardButton(text="Посмотреть услуги")
            ],
            [
                KeyboardButton(text="Назад в меню")
            ],
        ]
    )


def diagnostic_menu_reply_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Пройти расширенную диагностиĸу")
            ],
            [
                KeyboardButton(text="Базовая диагностиĸа")
            ],
            [
                KeyboardButton(text="Зачем мне диагностиĸа")
            ],
            [
                KeyboardButton(text="Назад в меню")
            ],
        ]
    )


def expanded_diagnostic_ready_reply_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Я готов(а), отправляю аудио")
            ],
            [
                KeyboardButton(text="Назад ĸ диагностиĸе")
            ],
            [
                KeyboardButton(text="Назад в меню")
            ],
        ]
    )


def expanded_diagnostic_upload_reply_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Назад ĸ диагностиĸе")
            ],
            [
                KeyboardButton(text="Назад в меню")
            ],
        ]
    )


def diagnostic_sent_reply_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Назад в меню")
            ],
        ]
    )


def basic_diagnostic_reply_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Пройти расширенную диагностиĸу")
            ],
            [
                KeyboardButton(text="Назад ĸ диагностиĸе")
            ],
            [
                KeyboardButton(text="Назад в меню")
            ],
        ]
    )
