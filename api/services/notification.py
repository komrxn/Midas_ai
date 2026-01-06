
import httpx
import logging
from ..config import get_settings
from ..models.user import User

logger = logging.getLogger(__name__)
settings = get_settings()

async def send_subscription_success_message(user: User):
    """
    Send a detailed success message with instructions to the user via Telegram Bot API.
    """
    if not user.telegram_id:
        return

    # TODO: Localize this message based on user.language
    lang = user.language or 'uz'
    
    # Message content based on language
    if lang == 'ru':
        message = (
            "🎉 **Поздравляем! Подписка активирована!** 🚀\n\n"
            "Теперь вам доступны все возможности **Baraka AI**:\n\n"
            "✅ **Безлимитные голосовые сообщения** — диктуйте траты на ходу.\n"
            "✅ **Сканирование чеков** — отправляйте фото чеков без ограничений.\n"
            "✅ **Управление долгами** — фиксируйте, кто вам должен и кому должны вы.\n"
            "✅ **Лимиты бюджетов** — ставьте ограничения на категории (например, «Еда»).\n"
            "✅ **Полная аналитика** — графики и статистика за любой период.\n\n"
            "⚙️ **Как пользоваться:**\n"
            "1. **Голос:** Просто скажите «Потратил 50000 на продукты».\n"
            "2. **Фото:** Отправьте фото чека, бот сам распознает товары.\n"
            "3. **Долги:** Скажите «Дал в долг Ахмеду 100 000 сум».\n"
            "4. **Лимиты:** Настройте в меню «Baraka AI PLUS» или в веб-приложении.\n\n"
            "Спасибо, что вы с нами! Если есть вопросы — нажмите «Инструкция»."
        )
    elif lang == 'en':
        message = (
            "🎉 **Congratulations! Subscription Activated!** 🚀\n\n"
            "You now have access to all **Baraka AI** features:\n\n"
            "✅ **Unlimited Voice Messages** — track expenses on the go.\n"
            "✅ **Receipt Scanning** — send photos of receipts without limits.\n"
            "✅ **Debt Management** — track who owes you and whom you owe.\n"
            "✅ **Budget Limits** — set limits for categories (e.g., 'Food').\n"
            "✅ **Full Analytics** — charts and statistics for any period.\n\n"
            "⚙️ **How to use:**\n"
            "1. **Voice:** Just say 'Spent 50000 on groceries'.\n"
            "2. **Photo:** Send a photo of a receipt, the bot will recognize items.\n"
            "3. **Debts:** Say 'Lent 100 000 UZS to Ahmed'.\n"
            "4. **Limits:** Configure in the 'Baraka AI PLUS' menu or web app.\n\n"
            "Thank you for being with us! If you have questions — press 'Instructions'."
        )
    else: # Default Uzbek
        message = (
            "🎉 **Tabriklaymiz! Obuna faollashtirildi!** 🚀\n\n"
            "Endi sizga **Baraka AI** ning barcha imkoniyatlari ochiq:\n\n"
            "✅ **Cheksiz ovozli xabarlar** — xarajatlarni yo'l-yo'lakay ayting.\n"
            "✅ **Cheklarni skanerlash** — chek rasmini cheklovsiz yuboring.\n"
            "✅ **Qarzlar nazorati** — kimdan qarzingiz bor va kim sizdan qarz ekanini yozib boring.\n"
            "✅ **Byudjet limitlari** — kategoriyalar uchun limit o'rnating (masalan, «Oziq-ovqat»).\n"
            "✅ **To'liq tahlil** — istalgan davr uchun grafiklar va statistika.\n\n"
            "⚙️ **Qanday ishlatiladi:**\n"
            "1. **Ovoz:** Shunchaki ayting «Bozorlikka 50000 ishlatdim».\n"
            "2. **Rasm:** Chek rasmini yuboring, bot tovarlarni o'zi aniqlaydi.\n"
            "3. **Qarzlar:** Ayting «Ahmadga 100 000 so'm qarz berdim».\n"
            "4. **Limitlar:** «Baraka AI PLUS» menyusida yoki veb-ilovada sozlang.\n\n"
            "Biz bilan bo'lganingiz uchun rahmat! Savollar bo'lsa — «Yo'riqnoma» tugmasini bosing."
        )

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
