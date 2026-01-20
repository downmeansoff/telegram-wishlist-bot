from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.models.wish import Wish, WishStatus
from app.bot.keyboards import (
    get_main_keyboard,
    get_groups_keyboard,
)

router = Router()


@router.callback_query(F.data == "main_menu")
async def callback_main_menu(callback: CallbackQuery):
    """Handle main menu callback"""
    await callback.message.edit_text(
        "🏠 <b>Главное меню</b>\n\n"
        "Выбери действие:",
        reply_markup=get_main_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "add_wish")
async def callback_add_wish(callback: CallbackQuery):
    """Handle add wish callback"""
    await callback.answer(
        "✍️ Напиши название желания в чат или используй Web App для полного функционала",
        show_alert=True
    )


@router.callback_query(F.data == "my_wishes")
async def callback_my_wishes(callback: CallbackQuery, session: AsyncSession, user: User):
    """Handle my wishes callback"""
    # Get wishes count
    result = await session.execute(
        select(Wish)
        .where(Wish.user_id == user.id)
        .where(Wish.status == WishStatus.ACTIVE)
    )
    wishes = result.scalars().all()

    wishes_text = f"📋 <b>Мой список желаний</b>\n\n"

    if not wishes:
        wishes_text += "Список пуст. Добавь первое желание!\n\n"
        wishes_text += "Используй /add или открой Web App 👇"
    else:
        wishes_text += f"Всего желаний: <b>{len(wishes)}</b>\n\n"
        wishes_text += "Открой Web App для управления списком 👇"

    await callback.message.edit_text(
        wishes_text,
        reply_markup=get_main_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "groups")
async def callback_groups(callback: CallbackQuery):
    """Handle groups callback"""
    groups_text = """
👥 <b>Групповые списки</b>

Создай группу для друзей или семьи:
• Делитесь желаниями
• Бронируйте подарки незаметно
• Получайте уведомления о днях рождения

Что делать дальше?
"""

    await callback.message.edit_text(
        groups_text,
        reply_markup=get_groups_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "create_group")
async def callback_create_group(callback: CallbackQuery):
    """Handle create group callback"""
    await callback.answer(
        "Создание групп доступно в Web App. Открой полный интерфейс! 🚀",
        show_alert=True
    )


@router.callback_query(F.data == "join_group")
async def callback_join_group(callback: CallbackQuery):
    """Handle join group callback"""
    await callback.answer(
        "Присоединение к группам доступно в Web App. Открой полный интерфейс! 🚀",
        show_alert=True
    )


@router.callback_query(F.data == "settings")
async def callback_settings(callback: CallbackQuery, user: User):
    """Handle settings callback"""
    settings_text = f"""
⚙️ <b>Настройки</b>

<b>Профиль:</b>
Имя: {user.full_name}
Username: {user.mention}
Язык: {user.language_code.upper()}

<b>Статистика:</b>
Всего желаний: загрузка...
Выполнено: загрузка...
Групп: загрузка...

Полные настройки доступны в Web App 👇
"""

    await callback.message.edit_text(
        settings_text,
        reply_markup=get_main_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("complete_wish:"))
async def callback_complete_wish(
    callback: CallbackQuery,
    session: AsyncSession,
    user: User
):
    """Handle complete wish callback"""
    wish_id = int(callback.data.split(":")[1])

    result = await session.execute(
        select(Wish).where(
            Wish.id == wish_id,
            Wish.user_id == user.id
        )
    )
    wish = result.scalar_one_or_none()

    if not wish:
        await callback.answer("❌ Желание не найдено", show_alert=True)
        return

    wish.status = WishStatus.COMPLETED
    await session.commit()

    await callback.answer("✅ Желание отмечено как выполненное!", show_alert=True)
    await callback.message.edit_text(
        f"✅ Поздравляю! Желание <b>{wish.title}</b> выполнено! 🎉",
        reply_markup=get_main_keyboard()
    )


@router.callback_query(F.data.startswith("delete_wish:"))
async def callback_delete_wish(
    callback: CallbackQuery,
    session: AsyncSession,
    user: User
):
    """Handle delete wish callback"""
    wish_id = int(callback.data.split(":")[1])

    result = await session.execute(
        select(Wish).where(
            Wish.id == wish_id,
            Wish.user_id == user.id
        )
    )
    wish = result.scalar_one_or_none()

    if not wish:
        await callback.answer("❌ Желание не найдено", show_alert=True)
        return

    await session.delete(wish)
    await session.commit()

    await callback.answer("🗑 Желание удалено", show_alert=True)
    await callback.message.edit_text(
        f"Желание <b>{wish.title}</b> удалено из списка.",
        reply_markup=get_main_keyboard()
    )
