"""Transaction confirmation handlers."""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler
from typing import Dict, Any

from .api_client import MidasAPIClient
from .config import config
from .user_storage import storage
from .pending_storage import pending_storage

logger = logging.getLogger(__name__)


async def show_transaction_confirmation(
    update: Update,
    user_id: int,
    tx_data: Dict[str, Any]
) -> str:
    """Show transaction confirmation with buttons."""
    # Store pending transaction
    tx_id = pending_storage.add(user_id, tx_data)
    
    # Format message
    tx_type = "💰 Доход" if tx_data['type'] == 'income' else "💸 Расход"
    amount_str = f"{tx_data['amount']:,.0f}".replace(',', ' ')
    currency = tx_data.get('currency', 'UZS').upper()
    
    # Get category name if available
    category_text = ""
    if tx_data.get('category_slug'):
        category_text = f"\n📁 Категория: {tx_data['category_slug']}"
    
    message = (
        f"{tx_type}\n"
        f"💵 Сумма: {amount_str} {currency}\n"
        f"📝 Описание: {tx_data['description']}"
        f"{category_text}\n\n"
        "Подтвердить?"
    )
    
    # Create buttons
    keyboard = [
        [
            InlineKeyboardButton("✅ Подтвердить", callback_data=f"confirm_{tx_id}"),
        ],
        [
            InlineKeyboardButton("❌ Отменить", callback_data=f"cancel_{tx_id}"),
            InlineKeyboardButton("✏️ Редактировать", callback_data=f"edit_{tx_id}"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Send message
    await update.message.reply_text(message, reply_markup=reply_markup)
    
    return tx_id


async def handle_transaction_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle transaction confirmation callbacks."""
    query = update.callback_query
    await query.answer()
    
    # Parse callback data
    action, tx_id = query.data.split('_', 1)
    
    # Get pending transaction
    pending = pending_storage.get(tx_id)
    if not pending:
        await query.edit_message_text("⏰ Время подтверждения истекло")
        return
    
    user_id = query.from_user.id
    if pending['user_id'] != user_id:
        await query.answer("❌ Это не твоя транзакция", show_alert=True)
        return
    
    tx_data = pending['tx_data']
    
    if action == "confirm":
        # Create transaction
        token = storage.get_user_token(user_id)
        api = MidasAPIClient(config.API_BASE_URL)
        api.set_token(token)
        
        try:
            # Get category_id from slug if provided
            if tx_data.get('category_slug'):
                categories = await api.get_categories()
                for cat in categories:
                    if cat.get('slug') == tx_data['category_slug']:
                        tx_data['category_id'] = cat['id']
                        break
                del tx_data['category_slug']  # Remove slug, keep only ID
            
            result = await api.create_transaction(tx_data)
            
            # Format success message
            amount_str = f"{tx_data['amount']:,.0f}".replace(',', ' ')
            tx_type = "доход" if tx_data['type'] == 'income' else "расход"
            
            await query.edit_message_text(
                f"✅ {tx_type.capitalize()} записан!\n"
                f"💵 {amount_str} {tx_data.get('currency', 'UZS').upper()}"
            )
            
            # Clean up
            pending_storage.remove(tx_id)
            
        except Exception as e:
            logger.error(f"Failed to create transaction: {e}")
            await query.edit_message_text(f"❌ Ошибка: {str(e)}")
    
    elif action == "cancel":
        await query.edit_message_text("❌ Отменено")
        pending_storage.remove(tx_id)
    
    elif action == "edit":
        # Start edit dialog
        await query.edit_message_text(
            "✏️ Редактирование транзакции\n\n"
            "Напиши новую сумму или описание:"
        )
        # Store edit state
        context.user_data['editing_tx'] = tx_id


# Export handler
transaction_callback_handler = CallbackQueryHandler(
    handle_transaction_callback,
    pattern="^(confirm|cancel|edit)_"
)
