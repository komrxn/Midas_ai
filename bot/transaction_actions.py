"""Transaction action handlers - Edit and Delete functionality."""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler
from typing import Dict, Any

from .api_client import MidasAPIClient
from .config import config
from .user_storage import storage
from .handlers.common import get_main_keyboard

logger = logging.getLogger(__name__)


async def show_transaction_with_actions(
    update: Update,
    user_id: int,
    tx_data: Dict[str, Any]
) -> None:
    """Show created transaction with Edit/Delete buttons."""
    tx_id = tx_data.get('transaction_id')
    amount = tx_data.get('amount', 0)
    desc = tx_data.get('description', '')
    tx_type = tx_data.get('type', 'expense')
    currency = tx_data.get('currency', 'uzs').upper()
    
    # Format message
    type_emoji = "💰" if tx_type == "income" else "💸"
    type_text = "Доход" if tx_type == "income" else "Расход"
    
    message = (
        f"✅ {type_text} записан!\n"
        f"{type_emoji} {amount:,.0f} {currency}\n"
        f"📝 {desc}"
    )
    
    # Create Edit/Delete buttons
    keyboard = [
        [
            InlineKeyboardButton("✏️ Редактировать", callback_data=f"edit_tx_{tx_id}"),
            InlineKeyboardButton("🗑 Удалить", callback_data=f"delete_tx_{tx_id}")
        ]
    ]
    
    await update.message.reply_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


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
    
    if action == "edit":
        # Start edit mode
        context.user_data['editing_transaction_id'] = tx_id
        await query.edit_message_text(
            "✏️ Редактирование транзакции\n\n"
            "Напиши новую сумму, описание или категорию:"
        )
        
    elif action == "delete":
        # Delete transaction
        try:
            await api.delete_transaction(tx_id)
            await query.edit_message_text("🗑 Удалено")
        except Exception as e:
            logger.error(f"Failed to delete transaction: {e}")
            await query.edit_message_text(f"❌ Ошибка: {str(e)}")


async def handle_edit_transaction_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle message when user is editing a transaction."""
    tx_id = context.user_data.pop('editing_transaction_id', None)
    if not tx_id:
        return False  # Not editing
    
    user_id = update.effective_user.id
    text = update.message.text
    
    token = storage.get_user_token(user_id)
    api = MidasAPIClient(config.API_BASE_URL)
    api.set_token(token)
    
    try:
        # Process edit with AI
        from .ai_agent import AIAgent
        agent = AIAgent(api)
        
        result = await agent.process_message(user_id, text)
        created_transactions = result.get("created_transactions", [])
        
        if created_transactions:
            # Get new data from AI parsed transaction
            new_data = created_transactions[0]
            
            # Update via API
            updates = {}
            if 'amount' in new_data:
                updates['amount'] = new_data['amount']
            if 'description' in new_data:
                updates['description'] = new_data['description']
            if 'category_slug' in new_data:
                # Convert slug to ID
                categories = await api.get_categories()
                for cat in categories:
                    if cat.get('slug') == new_data['category_slug']:
                        updates['category_id'] = cat['id']
                        break
            
            # Apply updates
            await api.update_transaction(tx_id, **updates)
            
            await update.message.reply_text(
                "✅ Обновлено!",
                reply_markup=get_main_keyboard()
            )
        else:
            await update.message.reply_text(
                "❌ Не понял. Попробуй ещё раз или отмени /start",
                reply_markup=get_main_keyboard()
            )
        
        return True  # Handled
        
    except Exception as e:
        logger.exception(f"Edit error: {e}")
        await update.message.reply_text(
            f"❌ Ошибка: {str(e)}",
            reply_markup=get_main_keyboard()
        )
        return True  # Handled


# Export handler
transaction_action_handler = CallbackQueryHandler(
    handle_transaction_action,
    pattern="^(edit|delete)_tx_"
)
