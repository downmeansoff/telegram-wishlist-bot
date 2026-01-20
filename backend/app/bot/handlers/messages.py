from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.wish import Wish, WishPriority
from app.bot.keyboards import get_main_keyboard

router = Router()


@router.message(F.text & ~F.text.startswith("/"))
async def handle_text_message(message: Message, session: AsyncSession, user: User):
    """Handle text messages - quick add wish"""

    # Ignore if too long or too short
    if len(message.text) < 3:
        await message.answer(
            "⚠️ Слишком короткое название. Попробуй ещё раз.",
            reply_markup=get_main_keyboard()
        )
        return

    if len(message.text) > 200:
        await message.answer(
            "⚠️ Слишком длинное название (макс. 200 символов).\n"
            "Используй Web App для подробного описания.",
            reply_markup=get_main_keyboard()
        )
        return

    # Create wish
    wish = Wish(
        user_id=user.id,
        title=message.text,
        priority=WishPriority.MEDIUM.value
    )

    session.add(wish)
    await session.commit()
    await session.refresh(wish)

    success_text = f"""
✅ <b>Желание добавлено!</b>

🎁 {wish.title}

Открой Web App, чтобы добавить:
• Фото
• Ссылку на товар
• Цену
• Категорию и приоритет
"""

    await message.answer(success_text, reply_markup=get_main_keyboard())


@router.message(F.photo)
async def handle_photo(message: Message):
    """Handle photo messages"""
    await message.answer(
        "📷 Фото получено!\n\n"
        "Для добавления желания с фото используй Web App - "
        "там можно добавить фото вместе с описанием, ценой и ссылкой! 👇",
        reply_markup=get_main_keyboard()
    )
