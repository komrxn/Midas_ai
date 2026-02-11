
import httpx
import logging
from ..config import get_settings
from ..models.user import User

logger = logging.getLogger(__name__)
settings = get_settings()

async def send_subscription_success_message(user: User, message_key: str = None):
    """
    Send a detailed success message with instructions to the user via Telegram Bot API.
    """
    if not user.telegram_id:
        return

    # Robust Translation Logic
    # We avoid importing bot.i18n to prevent path/dependency issues in API container
    import json
    from pathlib import Path
    
    lang = user.language or 'uz'
    
    # Calculate path to bot/locales relative to this file
    # This file: api/services/notification.py
    # Locales: bot/locales
    # Path: ../../../bot/locales
    try:
        current_file = Path(__file__)
        project_root = current_file.parent.parent.parent # api/services/ -> api/ -> root
        locales_dir = project_root / "bot" / "locales"
        
        # Load specific file: subscription.json
        lang_file = locales_dir / lang / "subscription.json"
        
        with open(lang_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        def get_text(key):
            # key format: subscription.success_trial -> we need just success_trial since we loaded subscription.json
            if key.startswith("subscription."):
                key = key.replace("subscription.", "")
            return data.get(key, key) # Return key if not found
            
    except Exception as e:
        logger.error(f"Failed to load translations in notification service: {e}")
        # Fallback to key
        def get_text(key): return key

    if message_key:
        message = get_text(message_key)
    else:
        # Fallback to logic based on subscription type
        sub_type = user.subscription_type or 'free'
        
        if sub_type == 'premium':
            message = get_text('success_premium')
        elif sub_type == 'pro':
            message = get_text('success_pro')
        elif sub_type == 'plus':
            message = get_text('success_plus')
        else:
            # For dynamic tier, we might not have it in this simple loader if it uses placeholders
            # But 'subscription_activated' uses {tier}.
            # Let's simple check
            raw_msg = get_text('subscription_activated')
            if raw_msg:
                message = raw_msg.replace("{tier}", sub_type.capitalize())
            else:
                message = f"Subscription {sub_type} activated!"

    # Send via Telegram Bot API
    url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"
    payload = {
        "chat_id": user.telegram_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(url, json=payload, timeout=10.0)
            resp.raise_for_status()
        except Exception as e:
            logger.error(f"Failed to send subscription success message: {e}")

async def send_subscription_expired_message(user: User):
    """
    Send subscription expired notification.
    """
    if not user.telegram_id:
        return

    lang = user.language or 'uz'
    
    if lang == 'ru':
        message = (
            "⏳ **Срок действия пробного периода истек**\n\n"
            "Ваш тариф изменен на **Free**.\n"
            "Чтобы вернуть безлимитные возможности и доступ к Premium AI, обновите подписку.\n\n"
            "👉 Нажмите кнопку **Baraka AI PLUS** в меню для выбора тарифа."
        )
    elif lang == 'en':
        message = (
            "⏳ **Trial period expired**\n\n"
            "Your plan has been changed to **Free**.\n"
            "To restore unlimited features and Premium AI access, please upgrade your subscription.\n\n"
            "👉 Press **Baraka AI PLUS** in the menu to select a plan."
        )
    else: # Default Uzbek
        message = (
            "⏳ **Sinov davri tugadi**\n\n"
            "Sizning tarifingiz **Free** ga o'zgartirildi.\n"
            "Cheksiz imkoniyatlar va Premium AI dan foydalanish uchun obunani yangilang.\n\n"
            "👉 Tarifni tanlash uchun menyuda **Baraka AI PLUS** tugmasini bosing."
        )

    url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"
    payload = {
        "chat_id": user.telegram_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(url, json=payload, timeout=10.0)
            resp.raise_for_status()
        except Exception as e:
            logger.error(f"Failed to send subscription expired message: {e}")
