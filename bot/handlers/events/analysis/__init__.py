from aiogram import Router

from .handlers import router as analysis_handlers

router = Router(name="analysis")
router.include_router(analysis_handlers)

__all__ = ["router"]
