from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User as TelegramUser
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal
from app.models.user import User
from sqlalchemy import select


class DatabaseMiddleware(BaseMiddleware):
    """Middleware to provide database session"""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        async with AsyncSessionLocal() as session:
            data["session"] = session

            # Get or create user
            telegram_user: TelegramUser = data.get("event_from_user")
            if telegram_user:
                user = await self.get_or_create_user(session, telegram_user)
                data["user"] = user

            return await handler(event, data)

    @staticmethod
    async def get_or_create_user(
        session: AsyncSession,
        telegram_user: TelegramUser
    ) -> User:
        """Get or create user from Telegram user data"""
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_user.id)
        )
        user = result.scalar_one_or_none()

        if not user:
            user = User(
                telegram_id=telegram_user.id,
                username=telegram_user.username,
                first_name=telegram_user.first_name,
                last_name=telegram_user.last_name,
                language_code=telegram_user.language_code or "ru",
                is_premium=telegram_user.is_premium or False,
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
        else:
            # Update user info if changed
            updated = False
            if user.username != telegram_user.username:
                user.username = telegram_user.username
                updated = True
            if user.first_name != telegram_user.first_name:
                user.first_name = telegram_user.first_name
                updated = True
            if user.last_name != telegram_user.last_name:
                user.last_name = telegram_user.last_name
                updated = True

            if updated:
                await session.commit()
                await session.refresh(user)

        return user
