from aiogram import Router

from app.bot.handlers import commands, callbacks, messages

router = Router()

# Include all handler routers
router.include_router(commands.router)
router.include_router(callbacks.router)
router.include_router(messages.router)

__all__ = ["router"]
