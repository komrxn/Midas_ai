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
        
        # Show login button
        login_text = "🔑 " + ("Kirish" if lang == 'uz' else ("Войти" if lang == 'ru' else "Login"))
        keyboard = [[KeyboardButton(login_text)]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        
        msg = {
            'uz': "⚠️ Avtorizatsiya kerak\n\nKirish uchun quyidagi tugmani bosing:",
            'ru': "⚠️ Требуется авторизация\n\nНажмите на кнопку ниже для входа:",
            'en': "⚠️ Authorization required\n\nClick the button below to login:"
        }.get(lang, "Authorization required")
        
        await update.message.reply_text(msg, reply_markup=reply_markup)
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
