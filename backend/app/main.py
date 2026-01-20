from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from app.core.config import settings
from app.api import wishes, users, groups

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url="/docs" if settings.is_development else None,
    redoc_url="/redoc" if settings.is_development else None,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS + ["https://web.telegram.org"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Global exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error" if settings.is_production else str(exc)
        }
    )


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "version": settings.VERSION
    }


# Include API routers
app.include_router(
    wishes.router,
    prefix=f"{settings.API_V1_STR}/wishes",
    tags=["wishes"]
)

app.include_router(
    users.router,
    prefix=f"{settings.API_V1_STR}/user",
    tags=["users"]
)

app.include_router(
    groups.router,
    prefix=f"{settings.API_V1_STR}/groups",
    tags=["groups"]
)


# Webhook endpoint for Telegram bot
@app.post("/api/webhook")
async def telegram_webhook(request: Request):
    """Telegram webhook endpoint"""
    try:
        from aiogram import Bot, Dispatcher
        from aiogram.types import Update
        from app.bot.handlers import router

        # Get update data
        data = await request.json()

        # Create bot instance
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        dp = Dispatcher()
        dp.include_router(router)

        # Process update
        await dp.feed_update(bot, Update(**data))

        return {"ok": True}

    except Exception as e:
        logger.error(f"Webhook error: {e}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


# Startup event
@app.on_event("startup")
async def startup_event():
    """Startup event"""
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Web App URL: {settings.WEB_APP_URL}")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event"""
    logger.info("Shutting down...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.is_development
    )
