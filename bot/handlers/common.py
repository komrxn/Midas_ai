"""Common utilities for handlers."""
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes
import logging

from ..user_storage import storage
from ..api_client import MidasAPIClient, UnauthorizedError

logger = logging.getLogger(__name__)


async def with_auth_check(update: Update, user_id: int, api_call):
    """Execute API call with automatic 401 error handling.
    
    If the API returns 401 Unauthorized (token expired), automatically:
    1. Clear the invalid token
    2. Prompt user to re-authenticate with /start
    3. Return None to indicate auth failure
    """
    try:
        return await api_call()
    except UnauthorizedError:
        # Token expired or invalid
        storage.clear_user_token(user_id)
        
        await update.message.reply_text(
            "🔑 **Твой токен авторизации истёк.**\n\n"
            "Отправь /start чтобы войти заново.",
            parse_mode='Markdown',
            reply_markup=ReplyKeyboardRemove()
        )
        logger.info(f"User {user_id} token expired, prompted to re-authenticate")
        return None
    except Exception as e:
        # Other errors - let them bubble up
        raise


def get_main_keyboard():
    """Get main menu keyboard."""
    keyboard = [
        [KeyboardButton("💰 Баланс"), KeyboardButton("📊 Статистика")],
        [KeyboardButton("❓ Помощь")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
