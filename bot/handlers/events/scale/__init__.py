__all__ = [
    "router"
]

from aiogram import Router

from .handlers import router as scale_handlers

router = Router(name="scale")
router.include_router(scale_handlers)