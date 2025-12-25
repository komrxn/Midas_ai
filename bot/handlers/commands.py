"""Command handlers."""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler
import logging

from ..user_storage import storage
from ..i18n import t
from .common import get_main_keyboard

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    user = update.effective_user
    user_id = user.id
    
    # Check if user is authorized
    if storage.is_user_authorized(user_id):
        # Existing user - show in their language
        lang = storage.get_user_language(user_id)
        
        await update.message.reply_text(
            t('auth.registration.welcome_back', lang, name=user.first_name),
            reply_markup=get_main_keyboard(lang)
        )
    else:
        # New user - show language selection FIRST
        keyboard = [
            [
                InlineKeyboardButton("🇷🇺 Русский", callback_data="startlang_ru"),
                InlineKeyboardButton("🇬🇧 English", callback_data="startlang_en"),
            ],
            [InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data="startlang_uz")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Show tri-lingual welcome
        message = (
            "👋 Assalomu alaykum!\n"
            "Bu bot Sizning shaxsiy moliyaviy yordamchingiz.\n\n"
            "👋 Здравствуйте!\n"
            "Этот бот — ваш личный финансовый помощник.\n\n"
            "👋 Hello!\n"
            "This bot is your personal finance assistant.\n\n"
            "🌐 Tilni tanlang / Выберите язык / Choose language:"
        )
        
        await update.message.reply_text(
            message,
            reply_markup=reply_markup
        )


async def start_language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle language selection at /start for new users."""
    query = update.callback_query
    await query.answer()
    
    # Extract language from callback_data: "startlang_ru" -> "ru"
    lang = query.data.split('_')[1]
    user_id = query.from_user.id
    
    # Save language preference
    storage.set_user_language(user_id, lang)
    
    # Show welcome message in selected language
    await query.edit_message_text(
        t('auth.registration.welcome_new', lang, name=query.from_user.first_name)
    )
    
    # Show registration/login buttons in selected language
    reg_text = "📝 " + ("Ro'yxatdan o'tish" if lang == 'uz' else ("Регистрация" if lang == 'ru' else "Register"))
    login_text = "🔑 " + ("Kirish" if lang == 'uz' else ("Войти" if lang == 'ru' else "Login"))
    
    keyboard = [
        [KeyboardButton(reg_text)],
        [KeyboardButton(login_text)]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    
    # Prompt to register or login
    prompt_msg = {
        'uz': "Davom etish uchun tanlang:",
        'ru': "Выберите действие:",
        'en': "Choose an action:"
    }.get(lang, "Choose:")
    
    await query.message.reply_text(prompt_msg, reply_markup=reply_markup)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    user_id = update.effective_user.id
    lang = storage.get_user_language(user_id)
    
    # Show language selection for help
    keyboard = [
        [
            InlineKeyboardButton("🇷🇺 Русский", callback_data="help_ru"),
            InlineKeyboardButton("🇬🇧 English", callback_data="help_en"),
        ],
        [InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data="help_uz")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        t('auth.common.choose_language', lang),
        reply_markup=reply_markup
    )


async def help_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show help in selected language."""
    query = update.callback_query
    await query.answer()
    
    # Extract language: "help_ru" -> "ru"
    lang = query.data.split('_')[1]
    
    help_text = t('help.full_guide', lang)
    
    await query.edit_message_text(
        help_text,
        parse_mode='Markdown'
    )


# Language selector callback handler
language_selector_handler = CallbackQueryHandler(start_language_callback, pattern="^startlang_")
help_selector_handler = CallbackQueryHandler(help_callback, pattern="^help_")
