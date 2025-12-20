"""Common utilities for handlers."""
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes
import logging

from ..user_storage import storage
from ..api_client import MidasAPIClient, UnauthorizedError
from ..i18n import t

logger = logging.getLogger(__name__)


async def with_auth_check(update: Update, user_id: int, api_call):
    """Execute API call with automatic 401 error handling."""
    try:
        return await api_call()
    except UnauthorizedError:
        storage.clear_user_token(user_id)
        lang = storage.get_user_language(user_id) or 'uz'
        
        await update.message.reply_text(
            t('auth.common.auth_required', lang),
            reply_markup=ReplyKeyboardRemove()
        )
        logger.info(f"User {user_id} token expired, prompted to re-authenticate")
        return None
    except Exception as e:
        raise


def get_main_keyboard(lang: str = 'uz'):
    """Get main menu keyboard with localized buttons."""
    keyboard = [
        [
            KeyboardButton(t('common.buttons.balance', lang)),
            KeyboardButton(t('common.buttons.statistics', lang))
        ],
        [KeyboardButton(t('common.buttons.instructions', lang))]
    ]
    
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
