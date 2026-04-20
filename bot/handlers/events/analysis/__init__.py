from aiogram import Router

from .callbacks import router as analysis_callbacks
from .handlers import router as analysis_handlers

router = Router(name="analysis")
router.include_router(analysis_handlers)
router.include_router(analysis_callbacks)

__all__ = ["router"]
