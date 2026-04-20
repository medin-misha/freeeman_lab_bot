__all__ = ["router", "broker"]

from aiogram import Router

from .handlers import router as nucleus_handlers
from .publisher import broker


router = Router(name="nucleus")
router.include_router(nucleus_handlers)
