from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo,
    ReplyKeyboardMarkup,
    KeyboardButton
)
from app.core.config import settings


def get_main_keyboard() -> InlineKeyboardMarkup:
    """Get main inline keyboard with Web App button"""
    buttons = []

    # Web App button only for HTTPS (production)
    if settings.WEB_APP_URL.startswith("https://"):
        buttons.append([
            InlineKeyboardButton(
                text="🎁 Мои желания",
                web_app=WebAppInfo(url=settings.WEB_APP_URL)
            )
        ])
    # For local development, skip Web App button (Telegram doesn't support localhost URLs)

    buttons.extend([
        [
            InlineKeyboardButton(
                text="➕ Добавить желание",
                callback_data="add_wish"
            ),
            InlineKeyboardButton(
                text="📋 Мой список",
                callback_data="my_wishes"
            )
        ],
        [
            InlineKeyboardButton(
                text="👥 Группы",
                callback_data="groups"
            ),
            InlineKeyboardButton(
                text="⚙️ Настройки",
                callback_data="settings"
            )
        ]
    ])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_wish_actions_keyboard(wish_id: int) -> InlineKeyboardMarkup:
    """Get keyboard for wish actions"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✏️ Редактировать",
                callback_data=f"edit_wish:{wish_id}"
            ),
            InlineKeyboardButton(
                text="✅ Выполнено",
                callback_data=f"complete_wish:{wish_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="🗑 Удалить",
                callback_data=f"delete_wish:{wish_id}"
            ),
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data="my_wishes"
            )
        ]
    ])
    return keyboard


def get_groups_keyboard() -> InlineKeyboardMarkup:
    """Get keyboard for groups"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="➕ Создать группу",
                callback_data="create_group"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔗 Присоединиться",
                callback_data="join_group"
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data="main_menu"
            )
        ]
    ])
    return keyboard


def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    """Get cancel keyboard for input states"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Отмена")]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard


def get_share_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """Get keyboard for sharing wish list"""
    share_url = f"{settings.WEB_APP_URL}?user={user_id}"

    buttons = []

    # Only add URL buttons for HTTPS (Telegram doesn't support localhost URLs)
    if settings.WEB_APP_URL.startswith("https://"):
        buttons.append([
            InlineKeyboardButton(
                text="📤 Поделиться",
                url=f"https://t.me/share/url?url={share_url}&text=Мой список желаний"
            )
        ])
        buttons.append([
            InlineKeyboardButton(
                text="🔗 Открыть в браузере",
                url=share_url
            )
        ])
    else:
        # For development, just show back button
        buttons.append([
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data="main_menu"
            )
        ])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
