"""Transaction action handlers - Edit and Delete functionality."""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler
from typing import Dict, Any
from datetime import datetime

from .api_client import MidasAPIClient
from .config import config
from .user_storage import storage
from .i18n import t, translate_category

logger = logging.getLogger(__name__)


async def show_transaction_with_actions(
    update: Update,
    user_id: int,
    tx_data: Dict[str, Any]
) -> None:
    """Show created transaction with Edit/Delete buttons."""
    tx_id = tx_data.get('transaction_id')
    lang = storage.get_user_language(user_id) or 'uz'
    
    # Fetch current balance
    api = MidasAPIClient(config.API_BASE_URL)
    api.set_token(storage.get_user_token(user_id))
    try:
        balance_data = await api.get_balance()
        balance_value = float(balance_data.get('balance', 0))
        currency = balance_data.get('currency', 'UZS').upper()
    except Exception as e:
        logger.warning(f"Could not fetch balance for tx message: {e}")
        balance_value = 0
        currency = 'UZS'

    # Transaction type
    type_val = tx_data.get('type', 'expense')
    type_emoji = t(f"transactions.type_emoji.{type_val}", lang)
    type_text = t(f"transactions.type.{type_val}", lang)
    
    # Amount formatting
    amount = float(tx_data.get('amount', 0))
    amount_formatted = f"{amount:,.0f}".replace(",", " ")
    currency_lower = tx_data.get('currency', 'UZS').lower()
    
    # Category translation
    category = tx_data.get('category')
    if isinstance(category, dict):
        category_slug = category.get('slug', '')
        category_name = translate_category(category_slug, lang) if category_slug else translate_category('general', lang)
    elif isinstance(category, str):
        category_name = translate_category(category, lang)
    else:
        category_name = translate_category('general', lang)
    
    # Description
    desc = tx_data.get('description', '')
    
    # Date
    date_str = datetime.now().strftime("%d.%m.%Y")

    # Construct message
    text = (
        f"**{t('transactions.created', lang)}**\n\n"
        f"{type_emoji} **{type_text}:**\n"
        f"{t('transactions.fields.date', lang)}: {date_str}\n\n"
        f"**{t('transactions.fields.amount', lang)}:** {currency_lower} {amount_formatted}\n"
        f"**{t('transactions.fields.category', lang)}:** {category_name}\n"
    )
    
    if desc:
        text += f"**{t('transactions.fields.description', lang)}:** {desc}\n"
    
    # Balance display
    balance_formatted = f"{balance_value:,.2f}".replace(",", " ")
    text += f"\n💰 {t('common.common.balance', lang)}: {currency.lower()} {balance_formatted}"

    # Buttons
    keyboard = [
        [
            InlineKeyboardButton(t('common.actions.cancel', lang), callback_data=f"delete_tx_{tx_id}"),
            InlineKeyboardButton(t('common.actions.edit', lang), callback_data=f"edit_tx_{tx_id}")
        ]
    ]
    
    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )
    
    logger.info(f"Transaction shown: {tx_id}")


async def handle_transaction_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle Edit/Delete callbacks."""
    query = update.callback_query
    await query.answer()
    
    parts = query.data.split('_')
    action = parts[0]
    tx_id = '_'.join(parts[2:])
    
    user_id = query.from_user.id
    lang = storage.get_user_language(user_id) or 'uz'
    token = storage.get_user_token(user_id)
    
    api = MidasAPIClient(config.API_BASE_URL)
    api.set_token(token)

    if action == "edit":
        context.user_data['editing_transaction_id'] = tx_id
        await query.edit_message_text(t('transactions.actions.edit_prompt', lang))
        
    elif action == "delete":
        try:
            await api.delete_transaction(tx_id)
            await query.edit_message_text(t('transactions.actions.deleted', lang))
        except Exception as e:
            logger.error(f"Failed to delete transaction: {e}")
            await query.edit_message_text(f"{t('common.common.error', lang)}: {str(e)}")


async def handle_edit_transaction_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle message when user is editing a transaction."""
    tx_id = context.user_data.pop('editing_transaction_id', None)
    if not tx_id:
        return False
    
    user_id = update.effective_user.id
    lang = storage.get_user_language(user_id) or 'uz'
    text = update.message.text
    
    token = storage.get_user_token(user_id)
    api = MidasAPIClient(config.API_BASE_URL)
    api.set_token(token)
    
    try:
        import re
        
        updates = {}
        
        # Parse amount with multipliers
        ming_match = re.search(r'(\d+(?:[.,]\d+)?)\s*(?:ming|минг)', text, re.IGNORECASE)
        k_match = re.search(r'(\d+(?:[.,]\d+)?)\s*k\b', text, re.IGNORECASE)
        plain_match = re.search(r'(\d+(?:[.,]\d+)?)', text)
        
        if ming_match:
            updates['amount'] = float(ming_match.group(1).replace(',', '.')) * 1000
        elif k_match:
            updates['amount'] = float(k_match.group(1).replace(',', '.')) * 1000
        elif plain_match:
            updates['amount'] = float(plain_match.group(1).replace(',', '.'))
        
        # Get description
        description = re.sub(r'\d+(?:[.,]\d+)?\s*(?:ming|минг|k)?', '', text, flags=re.IGNORECASE).strip()
        if description:
            updates['description'] = description
        
        if not updates:
            updates['description'] = text
        
        # Update transaction
        result = await api.update_transaction(tx_id, **updates)
        
        # Show updated transaction with correct category
        category_data = result.get('category', {})
        category_slug = category_data.get('slug', 'other_expense') if isinstance(category_data, dict) else 'other_expense'
        
        tx_data = {
            'transaction_id': str(result['id']),
            'amount': result.get('amount', 0),
            'description': result.get('description', ''),
            'type': result.get('type', 'expense'),
            'currency': result.get('currency', 'uzs'),
            'category': category_slug  # ← Pass slug for i18n translation!
        }
        
        await show_transaction_with_actions(update, user_id, tx_data)
        return True
        
    except Exception as e:
        logger.exception(f"Edit error: {e}")
        from .handlers.common import get_main_keyboard
        await update.message.reply_text(
            f"{t('common.common.error', lang)}: {str(e)}",
            reply_markup=get_main_keyboard(lang)
        )
        return True


# Export handler
transaction_action_handler = CallbackQueryHandler(
    handle_transaction_action,
    pattern="^(edit|delete)_tx_"
)
