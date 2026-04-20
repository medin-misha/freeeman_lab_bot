__all__ = ["router", "set_bot_instance"]

from aiogram import Router

from .rmq_subscriber import set_bot_instance


router = Router(name="nucleus")
