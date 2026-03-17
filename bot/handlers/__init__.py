from aiogram import Router
from .system.handlers import router as system_router
from .system.callbacks import router as system_callback_router


from .events.handlers import router as events_router

main_router = Router(name="main_router")
main_router.include_router(system_router)
main_router.include_router(system_callback_router)

main_router.include_router(events_router)

__all__ = [
    "main_router"
]
