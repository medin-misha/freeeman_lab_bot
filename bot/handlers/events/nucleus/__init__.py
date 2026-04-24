__all__ = ["router"]

from aiogram import Router

from .handlers import router as nucleus_handlers


router = Router(name="nucleus")
router.include_router(nucleus_handlers)
