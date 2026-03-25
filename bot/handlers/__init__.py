from aiogram import Router
from .system.handlers import router as system_router
from .system.callbacks import router as system_callback_router


from .events.scale import router as scale_router
from .events.analysis import router as analysis_router
from .events.diagnostics import router as diagnostics_router
main_router = Router(name="main_router")
main_router.include_router(system_router)
main_router.include_router(system_callback_router)

main_router.include_router(scale_router)
main_router.include_router(analysis_router)
main_router.include_router(diagnostics_router)

__all__ = [
    "main_router"
]
