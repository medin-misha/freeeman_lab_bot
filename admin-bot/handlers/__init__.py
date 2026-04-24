from aiogram import Router

from .events.analysis import router as analysis_router
from .events.consultations import router as consultations_router
from .events.diagnostics import router as diagnostics_router
from .events.mentorship import router as mentorship_router
from .events.regressions import router as regressions_router
from .events.nucleus import router as nucleus_router
from .system.handlers import router as system_router


main_router = Router(name="main_router")
main_router.include_router(system_router)
main_router.include_router(analysis_router)
main_router.include_router(consultations_router)
main_router.include_router(mentorship_router)
main_router.include_router(regressions_router)
main_router.include_router(diagnostics_router)
main_router.include_router(nucleus_router)


__all__ = ["main_router"]
