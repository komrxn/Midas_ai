from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler
from bot.api_client import BarakaAPIClient
from bot.config import config
from bot.i18n import t
from bot.user_storage import storage

async def activate_trial_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle trial activation callback."""
    query = update.callback_query
    # We might need language for notifications, let's get it
    user_id = query.from_user.id
    lang = storage.get_user_language(user_id) or 'uz'
    
    await query.answer()
    
    token = storage.get_user_token(user_id)
    api = BarakaAPIClient(config.API_BASE_URL)
    api.set_token(token)
    
    try:
        data = await api.activate_trial()
        
        expires = data.get("expires_at", "soon")
        text = (
            f"{t('subscription.trial_activated_title', lang)}\n\n"
            f"{t('subscription.trial_activated_body', lang, date=expires)}"
        )
        await query.edit_message_text(text, parse_mode="Markdown")
        
    except Exception as e:
        status_code = getattr(e, "response", None) and e.response.status_code
        if status_code == 400:
             await query.edit_message_text(t("subscription.trial_already_used", lang), parse_mode="Markdown")
        else:
             await query.edit_message_text(t("subscription.trial_error", lang), parse_mode="Markdown")

async def buy_subscription_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle buy subscription callback."""
    query = update.callback_query
    user_id = query.from_user.id
    lang = storage.get_user_language(user_id) or 'uz'
    
    await query.answer()
    
    # Simple menu for now
    keyboard = [
        [InlineKeyboardButton(t("subscription.monthly_plan_btn", lang, price="19,990"), callback_data="pay_monthly")],
        # [InlineKeyboardButton("Annual Plan - 150,000 UZS", callback_data="pay_annual")], # Not implemented yet
        [InlineKeyboardButton(t("subscription.back_btn", lang), callback_data="profile_menu")] 
    ]
    await query.edit_message_text(
        f"{t('subscription.select_plan_title', lang)}\n\n"
        f"{t('subscription.select_plan_body', lang)}",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def pay_monthly_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate payment link."""
    query = update.callback_query
    user_id = query.from_user.id
    lang = storage.get_user_language(user_id) or 'uz'
    
    await query.answer(t("common.common.loading", lang))
    
    token = storage.get_user_token(user_id)
    api = BarakaAPIClient(config.API_BASE_URL)
    api.set_token(token)
    
    try:
        data = await api.generate_payment_link(plan_id="monthly")
        url = data.get("url")
        
        keyboard = [
            [InlineKeyboardButton(t("subscription.pay_click_btn", lang), url=url)],
            [InlineKeyboardButton(t("subscription.back_btn", lang), callback_data="buy_subscription")]
        ]
        
        await query.edit_message_text(
            f"{t('subscription.payment_initiated', lang)}\n\n"
            f"{t('subscription.payment_instructions', lang)}",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
    except Exception as e:
        await query.edit_message_text(f"❌ Error generating link: {str(e)}", parse_mode="Markdown")

subscription_handlers = [
    CallbackQueryHandler(activate_trial_callback, pattern="^activate_trial$"),
    CallbackQueryHandler(buy_subscription_callback, pattern="^buy_subscription$"),
    CallbackQueryHandler(pay_monthly_callback, pattern="^pay_monthly$"),
]
