import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from app.core.config import settings
from app.bot.handlers import router
from app.bot.middleware import DatabaseMiddleware

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Main bot function"""
    # Initialize bot and dispatcher
    bot = Bot(
        token=settings.TELEGRAM_BOT_TOKEN,
        parse_mode=ParseMode.HTML
    )

    dp = Dispatcher()

    # Register middleware
    dp.update.middleware(DatabaseMiddleware())

    # Register routers
    dp.include_router(router)

    # Start polling or webhook
    try:
        logger.info("Starting bot...")

        if settings.TELEGRAM_BOT_WEBHOOK_URL:
            # Webhook mode (for production)
            logger.info(f"Setting webhook: {settings.TELEGRAM_BOT_WEBHOOK_URL}")
            await bot.set_webhook(
                url=settings.TELEGRAM_BOT_WEBHOOK_URL,
                drop_pending_updates=True
            )
            logger.info("Webhook set successfully. Bot is running...")
            # Keep the script running
            await asyncio.Event().wait()
        else:
            # Polling mode (for development)
            logger.info("Starting polling...")
            await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
