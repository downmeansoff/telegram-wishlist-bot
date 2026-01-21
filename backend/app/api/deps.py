import json
from typing import Optional
from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import verify_telegram_web_app_data
from app.models.user import User


async def get_current_user(
    x_telegram_init_data: str = Header(...),
    session: AsyncSession = Depends(get_db)
) -> User:
    """
    Get current user from Telegram Web App initData

    Args:
        x_telegram_init_data: Telegram Web App initData from header
        session: Database session

    Returns:
        User: Current user

    Raises:
        HTTPException: If user not found or invalid data
    """
    # Verify and parse init data
    parsed_data = verify_telegram_web_app_data(x_telegram_init_data)

    # Get user data from parsed data (use json.loads instead of eval for safety)
    user_json = parsed_data.get("user", "{}")
    user_data = json.loads(user_json) if isinstance(user_json, str) else user_json
    telegram_id = user_data.get("id")

    if not telegram_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found in init data"
        )

    # Get user from database
    result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        # Create user if not exists
        user = User(
            telegram_id=telegram_id,
            username=user_data.get("username"),
            first_name=user_data.get("first_name", "User"),
            last_name=user_data.get("last_name"),
            language_code=user_data.get("language_code", "ru"),
            is_premium=user_data.get("is_premium", False),
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)

    return user


async def get_current_user_optional(
    x_telegram_init_data: Optional[str] = Header(None),
    session: AsyncSession = Depends(get_db)
) -> Optional[User]:
    """Get current user (optional) - for public endpoints"""
    if not x_telegram_init_data:
        return None

    try:
        return await get_current_user(x_telegram_init_data, session)
    except HTTPException:
        return None
