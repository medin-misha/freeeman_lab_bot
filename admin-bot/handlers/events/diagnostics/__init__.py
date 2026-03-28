__all__ = ["router", "broker", "set_bot_instance"]

from aiogram import Router

from .callbacks import router as diagnostics_callbacks
from .handlers import router as diagnostics_handlers
from .rmq_subscriber import broker, set_bot_instance


router = Router(name="diagnostics")
router.include_router(diagnostics_handlers)
router.include_router(diagnostics_callbacks)
