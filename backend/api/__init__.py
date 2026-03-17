from fastapi import APIRouter
from .v1.users.views import router as users_router

main_router = APIRouter()

main_router.include_router(users_router)

__all__ = ["main_router"]