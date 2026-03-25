from fastapi import APIRouter
from .v1.diagnostics.views import router as diagnostics_router
from .v1.users.views import router as users_router
from .v1.files.views import router as files_router

main_router = APIRouter()

main_router.include_router(users_router)
main_router.include_router(files_router)
main_router.include_router(diagnostics_router)

__all__ = ["main_router"]
