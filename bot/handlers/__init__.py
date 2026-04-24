from aiogram import Router
from .errors import router as errors_router
from .system.handlers import router as system_router
from .system.callbacks import router as system_callback_router
from .events.scale import router as scale_router
from .events.analysis import router as analysis_router
from .events.nucleus import router as nucleus_router
from .events.diagnostics import router as diagnostics_router
from .events.more import router as more_router

main_router = Router(name="main_router")
# more_router первым, чтобы его state-фильтры (напр. MoreStates.shop + "Назад")
# имели приоритет над безусловным back_to_menu_handler в system_router
main_router.include_router(more_router)
main_router.include_router(system_router)
main_router.include_router(system_callback_router)
main_router.include_router(scale_router)
main_router.include_router(analysis_router)
main_router.include_router(nucleus_router)
main_router.include_router(diagnostics_router)


# должен быть последним
main_router.include_router(errors_router)
__all__ = [
    "main_router"
]
