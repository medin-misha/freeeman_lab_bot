from aiogram import Router
from .handlers import router as more_handlers

router = Router(name="more")
router.include_router(more_handlers)

__all__ = ["router"]
