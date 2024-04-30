__all__ = ("router")

from aiogram import Router
from .user_handler import router as user_router
from .media_handler import router as media_router
from .twitter_handler import router as twitter_router

router = Router()
router.include_routers(
    user_router,
    media_router,
    twitter_router,
)