"""Common utilities for handlers."""
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes
import logging

from ..user_storage import storage
from ..api_client import MidasAPIClient, UnauthorizedError

from ..lang_messages import get_message

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
        
        # Get user language for error message (default to 'uz' if unknown, though auth failed so maybe unknown)
        lang = storage.get_user_language(user_id) or 'uz'
        
        await update.message.reply_text(
            get_message(lang, 'auth_required'),
            reply_markup=ReplyKeyboardRemove()
        )
        logger.info(f"User {user_id} token expired, prompted to re-authenticate")
        return None
    except Exception as e:
        # Other errors - let them bubble up
        raise


def get_main_keyboard(lang: str = 'uz'):
    """Get main menu keyboard."""
    keyboard = [
        [KeyboardButton(get_message(lang, 'balance')), KeyboardButton(get_message(lang, 'statistics_title'))],
        [KeyboardButton(get_message(lang, 'instructions_btn'))]
    ]
    # Check if 'help' key exists, if not use hardcoded or add it. 
    # Current lang_messages doesn't have 'help'. I should add valid keys.
    # 'balance' -> "💰 Balance"
    # 'statistics_title' -> "📊 Statistics"
    # I should add 'help_btn' to lang_messages? Or just use "Help"
    
    # For now, let's stick to what we have in keys. 
    # Wait, 'balance' in messages is "💰 Balance". 
    # 'statistics_title' is "📊 Statistics".
    
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
