__all__ = [
    "router", "broker", "set_bot_instance"
]

from aiogram import Router

from .rmq_subscriber import broker, set_bot_instance
from handlers.events.diagnostics.handlers import router as diagnostics_handlers
from handlers.events.diagnostics.callbacks import router as diagnostics_callbacks

router = Router(name="diagnostics")
router.include_router(diagnostics_handlers)
router.include_router(diagnostics_callbacks)
