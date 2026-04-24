from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


def back_reply_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Назад")],
        ]
    )


def more_reply_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Посмотреть услуги")],
            [KeyboardButton(text="Соцсети")],
            [KeyboardButton(text="Магазин")],
            [KeyboardButton(text="О проекте")],
            [KeyboardButton(text="Назад в меню")],
        ]
    )


def consultations_reply_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Оставить запрос")],
            [KeyboardButton(text="Назад")],
        ]
    )


def services_reply_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Консультации")],
            [KeyboardButton(text="Регрессии")],
            [KeyboardButton(text="Наставничество")],
            [KeyboardButton(text="Назад")],
        ]
    )


def socials_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="YouTube",
                    url="https://www.youtube.com/@Freemanlifelab",
                )
            ],
            [
                InlineKeyboardButton(
                    text="RuTube",
                    url="https://rutube.ru/channel/69126193/",
                )
            ],
            [
                InlineKeyboardButton(
                    text="Telegram",
                    url="https://t.me/alexfreemanlifelab",
                )
            ],
            [
                InlineKeyboardButton(
                    text="Сайт",
                    url="https://freemanalexander.ru",
                )
            ],
            [
                InlineKeyboardButton(
                    text="VK",
                    url="https://vk.com/freemanlifelab",
                )
            ],
            [
                InlineKeyboardButton(
                    text="Instagram",
                    url="https://instagram.com/freemanlifelab",
                )
            ],
        ]
    )
