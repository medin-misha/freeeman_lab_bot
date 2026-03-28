from aiogram import Router

from .events.diagnostics import router as diagnostics_router
from .system.handlers import router as system_router


main_router = Router(name="main_router")
main_router.include_router(system_router)
main_router.include_router(diagnostics_router)


__all__ = ["main_router"]
