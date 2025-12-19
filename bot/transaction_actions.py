"""Transaction action handlers - Edit and Delete functionality."""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler
from typing import Dict, Any

from .api_client import MidasAPIClient
from .config import config
from .user_storage import storage
from .handlers.common import get_main_keyboard
from .lang_messages import get_message

logger = logging.getLogger(__name__)


async def show_transaction_with_actions(
    update: Update,
    user_id: int,
    tx_data: Dict[str, Any]
) -> None:
    """Show created transaction with Edit/Delete buttons."""
    tx_id = tx_data.get('transaction_id')
    # Get localized strings
    lang = storage.get_user_language(user_id) or 'uz'
    
    # Fetch current balance
    api = MidasAPIClient(config.API_BASE_URL)
    api.set_token(storage.get_user_token(user_id))
    try:
        balance_data = await api.get_balance()
        balance_value = float(balance_data.get('balance', 0))
        currency = balance_data.get('currency', 'UZS')
        # Hardcoded USD balance for now or fetch if available?
        # Assuming only single currency for MVP, but user asked for USD too.
        # Let's just show main currency.
    except Exception as e:
        logger.warning(f"Could not fetch balance for tx message: {e}")
        balance_value = 0
        currency = 'UZS'

    type_emoji = "💸" if tx_data['type'] == 'expense' else "💰"
    type_text = get_message(lang, 'income') if tx_data['type'] == 'income' else get_message(lang, 'expense')
    amount_text = f"{tx_data.get('currency', 'UZS')} {float(tx_data['amount']):,.0f}".replace(",", " ")
    
    desc = tx_data.get('description', '')
    category = tx_data.get('category', {})
    category_name = category.get('name', 'General') if isinstance(category, dict) else str(category)
    
    # Date (using current date or tx date)
    from datetime import datetime
    date_str = datetime.now().strftime("%d.%m.%Y")

    # Construct Message
    # Добавлено в отчет ✅
    #
    # 💸 Расход:
    # Дата: 18.12.2025
    #
    # Сумма: UZS 20 000
    # Категория: Транспорт
    # Описание: Такси
    #
    # Баланс: UZS (so'm): 1 210 000.00
    
    text = (
        f"**{get_message(lang, 'added_to_report')}**\n\n"
        f"{type_emoji} **{type_text}:**\n"
        f"{get_message(lang, 'date_label')}: {date_str}\n\n"
        f"**{get_message(lang, 'amount_label')}:** {amount_text}\n"
        f"**{get_message(lang, 'category_label')}:** {category_name}\n"
    )
    
    if desc:
        text += f"**{get_message(lang, 'desc_label')}:** {desc}\n"
        
    text += f"\n**{get_message(lang, 'balance')}:** {currency} {balance_value:,.2f}".replace(",", " ")

    keyboard = [
        [
            InlineKeyboardButton(f"{get_message(lang, 'cancel_btn')}", callback_data=f"delete_tx_{tx_id}"),
            InlineKeyboardButton(f"{get_message(lang, 'edit_btn')}", callback_data=f"edit_tx_{tx_id}")
        ]
    ]
    
    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )
    
    # Also log transaction
    logger.info(f"Transaction shown: {tx_id}")


async def handle_transaction_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle Edit/Delete callbacks."""
    query = update.callback_query
    await query.answer()
    
    # Parse: "edit_tx_123" or "delete_tx_123"
    parts = query.data.split('_')
    action = parts[0]  # "edit" or "delete"
    tx_id = '_'.join(parts[2:])  # transaction ID (might contain underscores)
    
    user_id = query.from_user.id
    token = storage.get_user_token(user_id)
    api = MidasAPIClient(config.API_BASE_URL)
    api.set_token(token)
    
    # Get localized strings (reuse user_id from query)
    # Note: query.from_user.id is used above
    lang = storage.get_user_language(user_id) or 'uz'

    if action == "edit":
        # Start edit mode
        context.user_data['editing_transaction_id'] = tx_id
        await query.edit_message_text(get_message(lang, 'edit_prompt'))
        
    elif action == "delete":
        # Delete transaction
        try:
            await api.delete_transaction(tx_id)
            await query.edit_message_text(get_message(lang, 'deleted'))
        except Exception as e:
            logger.error(f"Failed to delete transaction: {e}")
            await query.edit_message_text(f"❌ {get_message(lang, 'error_generic')}: {str(e)}")


async def handle_edit_transaction_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle message when user is editing a transaction."""
    tx_id = context.user_data.pop('editing_transaction_id', None)
    if not tx_id:
        return False  # Not editing
    
    user_id = update.effective_user.id
    lang = storage.get_user_language(user_id) or 'uz'
    text = update.message.text
    
    token = storage.get_user_token(user_id)
    api = MidasAPIClient(config.API_BASE_URL)
    api.set_token(token)
    
    try:
        # Parse the edit text to extract updates
        # Support "50ming", "50k" etc for thousands
        import re
        
        updates = {}
        
        # Check for multipliers first (ming, k)
        ming_match = re.search(r'(\d+(?:[.,]\d+)?)\s*(?:ming|минг)', text, re.IGNORECASE)
        k_match = re.search(r'(\d+(?:[.,]\d+)?)\s*k\b', text, re.IGNORECASE)
        plain_match = re.search(r'(\d+(?:[.,]\d+)?)', text)
        
        if ming_match:
            updates['amount'] = float(ming_match.group(1).replace(',', '.')) * 1000
        elif k_match:
            updates['amount'] = float(k_match.group(1).replace(',', '.')) * 1000
        elif plain_match:
            updates['amount'] = float(plain_match.group(1).replace(',', '.'))
        
        # Get description (remove numbers and multipliers)
        description = re.sub(r'\d+(?:[.,]\d+)?\s*(?:ming|минг|k)?', '', text, flags=re.IGNORECASE).strip()
        if description:
            updates['description'] = description
        
        # If no changes detected, use whole text as description
        if not updates:
            updates['description'] = text
        
        # Update transaction
        result = await api.update_transaction(tx_id, **updates)
        
        # Show updated transaction with Edit/Delete buttons
        tx_data = {
            'transaction_id': str(result['id']),
            'amount': result.get('amount', 0),
            'description': result.get('description', ''),
            'type': result.get('type', 'expense'),
            'currency': result.get('currency', 'uzs')
        }
        
        await show_transaction_with_actions(update, user_id, tx_data)
        
        return True  # Handled
        
    except Exception as e:
        logger.exception(f"Edit error: {e}")
        await update.message.reply_text(
            f"❌ {get_message(lang, 'error_generic')}: {str(e)}",
            reply_markup=get_main_keyboard(lang)
        )
        return True  # Handled


# Export handler
transaction_action_handler = CallbackQueryHandler(
    handle_transaction_action,
    pattern="^(edit|delete)_tx_"
)
