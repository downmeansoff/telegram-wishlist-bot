from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.user import User
from app.models.wish import Wish, WishStatus
from app.bot.keyboards import (
    get_main_keyboard,
    get_share_keyboard,
)
from app.core.config import settings

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, user: User):
    """Handle /start command"""
    welcome_text = f"""
👋 <b>Привет, {user.first_name}!</b>

Добро пожаловать в <b>Wish List Bot</b> - твой личный менеджер желаний! 🎁

Здесь ты можешь:
✨ Создавать списки желаний
🎯 Управлять приоритетами
👥 Делиться списками с друзьями
🎂 Создавать групповые списки для дней рождения

<b>Основные команды:</b>
• /add - Добавить желание
• /list - Посмотреть список
• /share - Поделиться списком
• /help - Справка

<b>Быстрое добавление:</b>
Просто напиши название желания, и я добавлю его в список!
Например: "iPhone 15 Pro"
"""

    # Add Web App info only for HTTPS
    if settings.WEB_APP_URL.startswith("https://"):
        welcome_text += "\n💡 Нажми кнопку ниже для полного функционала Web App!"

    await message.answer(welcome_text, reply_markup=get_main_keyboard())


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Handle /help command"""
    help_text = """
📖 <b>Справка по командам:</b>

<b>Основные команды:</b>
/start - Главное меню
/add - Быстро добавить желание
/list - Показать мой список (топ-5)
/share - Поделиться списком
/help - Эта справка

<b>Как пользоваться:</b>
1. Нажми кнопку "🎁 Мои желания" для открытия полного интерфейса
2. Добавляй желания с фото, ссылками и ценой
3. Создавай группы и приглашай друзей
4. Бронируй подарки в группах (невидимо для получателя)

<b>Групповые списки:</b>
• Создай группу для семьи/друзей
• Добавь свои желания
• Смотри желания других участников
• Бронируй подарки незаметно

<b>Нужна помощь?</b> Пиши @support
"""

    await message.answer(help_text, reply_markup=get_main_keyboard())


@router.message(Command("add"))
async def cmd_add(message: Message):
    """Handle /add command"""
    add_text = """
➕ <b>Добавить желание</b>

Просто напиши название желания, и я добавлю его в твой список!

Например:
• iPhone 15 Pro
• Книга "Мастер и Маргарита"
• Абонемент в спортзал

Или открой Web App для добавления с фото и подробностями 👇
"""

    await message.answer(add_text, reply_markup=get_main_keyboard())


@router.message(Command("list"))
async def cmd_list(message: Message, session: AsyncSession, user: User):
    """Handle /list command"""
    # Get user's wishes
    result = await session.execute(
        select(Wish)
        .where(Wish.user_id == user.id)
        .where(Wish.status == WishStatus.ACTIVE)
        .order_by(Wish.priority.desc(), Wish.created_at.desc())
        .limit(5)
    )
    wishes = result.scalars().all()

    if not wishes:
        await message.answer(
            "📝 Твой список желаний пока пуст.\n\n"
            "Добавь первое желание командой /add или через Web App 👇",
            reply_markup=get_main_keyboard()
        )
        return

    # Get total count
    total_result = await session.execute(
        select(func.count(Wish.id))
        .where(Wish.user_id == user.id)
        .where(Wish.status == WishStatus.ACTIVE)
    )
    total_count = total_result.scalar()

    # Format wishes
    wishes_text = "🎁 <b>Твои желания (топ-5):</b>\n\n"

    priority_emoji = {1: "🟢", 2: "🟡", 3: "🔴", 4: "⚡"}

    for i, wish in enumerate(wishes, 1):
        emoji = priority_emoji.get(wish.priority, "⚪")
        price_text = f" • {wish.formatted_price}" if wish.price else ""
        wishes_text += f"{i}. {emoji} <b>{wish.title}</b>{price_text}\n"

        if wish.description:
            desc = wish.description[:50] + "..." if len(wish.description) > 50 else wish.description
            wishes_text += f"   <i>{desc}</i>\n"

        wishes_text += "\n"

    if total_count > 5:
        wishes_text += f"\nВсего желаний: <b>{total_count}</b>\n"
        wishes_text += "Открой полный список в Web App 👇"

    await message.answer(wishes_text, reply_markup=get_main_keyboard())


@router.message(Command("share"))
async def cmd_share(message: Message, user: User):
    """Handle /share command"""
    if settings.WEB_APP_URL.startswith("https://"):
        share_text = f"""
📤 <b>Поделиться списком желаний</b>

Отправь эту ссылку друзьям или семье, чтобы они увидели твои желания:

👉 {settings.WEB_APP_URL}?user={user.id}

Или используй кнопку ниже 👇
"""
    else:
        share_text = f"""
📤 <b>Поделиться списком желаний</b>

⚠️ В режиме разработки функция "Поделиться" недоступна.

Для полного функционала задеплойте приложение на HTTPS сервер.

Пока используйте команды:
• /list - Посмотреть список
• /add - Добавить желание
"""

    await message.answer(share_text, reply_markup=get_share_keyboard(user.id))
