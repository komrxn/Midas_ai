"""Balance handler."""
from telegram import Update
from telegram.ext import ContextTypes
import logging

from ..user_storage import storage
from ..api_client import MidasAPIClient
from ..config import config
from .common import with_auth_check, get_main_keyboard

logger = logging.getLogger(__name__)


async def get_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get user balance and show stats."""
    if not storage.is_user_authorized(update.effective_user.id):
        await update.message.reply_text("⛔ Сначала авторизуйся: /start")
        return
    
    user_id = update.effective_user.id
    token = storage.get_user_token(user_id)
    api = MidasAPIClient(config.API_BASE_URL)
    api.set_token(token)
    
    async def _get_balance():
        balance = await api.get_balance(period="month")
        return balance
    
    balance = await with_auth_check(update, user_id, _get_balance)
    if balance is None:
        return  # Auth failed
    
    # Convert to float (API returns strings)
    income = float(balance.get("income", 0))
    expense = float(balance.get("expense", 0))
    total = float(balance.get("balance", 0))
    currency = balance.get("currency", "UZS")
    
    await update.message.reply_text(
        f"💰 **Баланс за месяц**\n\n"
        f"📈 Доход: {income:,.0f} {currency}\n"
        f"📉 Расход: {expense:,.0f} {currency}\n"
        f"💵 Итого: {total:,.0f} {currency}",
        parse_mode='Markdown',
        reply_markup=get_main_keyboard()
    )
