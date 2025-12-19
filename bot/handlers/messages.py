"""Message handler module."""
import logging
from telegram import Update
from telegram.ext import ContextTypes

from ..ai_agent import AIAgent
from ..api_client import MidasAPIClient
from ..config import config
from ..user_storage import storage
from ..transaction_actions import show_transaction_with_actions, handle_edit_transaction_message
from .common import with_auth_check, get_main_keyboard
from ..lang_messages import get_message

logger = logging.getLogger(__name__)


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages with AI."""
    user_id = update.effective_user.id
    
    # Auth check
    if not storage.is_user_authorized(user_id):
        lang = storage.get_user_language(user_id) or 'uz'
        await update.message.reply_text(get_message(lang, 'auth_required'))
        return
    
    text = update.message.text
    
    # Check if user is editing a transaction
    if context.user_data.get('editing_tx'):
        from ..confirmation_handlers import handle_edit_message
        await handle_edit_message(update, context)
        return
    
    await process_text_message(update, context, text, user_id)


async def process_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, user_id: int):
    """Process any text message (typed or transcribed) through the main pipeline."""
async def process_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, user_id: int):
    """Process any text message (typed or transcribed) through the main pipeline."""
    # Get user language first to handle localized buttons
    lang = storage.get_user_language(user_id) or 'uz'
    
    # Handle menu buttons first
    if text == get_message(lang, 'balance'):
        token = storage.get_user_token(user_id)
        api = MidasAPIClient(config.API_BASE_URL)
        api.set_token(token)
        await show_balance(update, api, lang)
        return
    elif text == get_message(lang, 'statistics_title'):
        # Show statistics (keep existing functionality)
        token = storage.get_user_token(user_id)
        api = MidasAPIClient(config.API_BASE_URL)
        api.set_token(token)
        await show_statistics(update, api, lang)
        return
    elif text == "❓ Help" or text == "❓ Yordam" or text == "❓ Помощь": # Needs proper key in future
        from .commands import help_command
        await help_command(update, context)
        return
    
    # Check if user is editing a transaction (action buttons flow)
    is_editing = await handle_edit_transaction_message(update, context)
    if is_editing:
        return  # Edit handled
    
    # Get token and API client
    token = storage.get_user_token(user_id)
    api = MidasAPIClient(config.API_BASE_URL)
    api.set_token(token)
    
    # Process with AI
    agent = AIAgent(api)
    result = await agent.process_message(user_id, text)
    
    response_text = result.get("response", "")
    created_transactions = result.get("created_transactions", [])
    
    # Show AI response
    if not created_transactions and response_text:
        try:
            await update.message.reply_text(
                response_text,
                parse_mode='Markdown',
                reply_markup=get_main_keyboard()
            )
        except Exception:
            await update.message.reply_text(
                response_text,
                reply_markup=get_main_keyboard()
            )
            
    # Show each created transaction with Edit/Delete buttons
    if created_transactions:
        # If there's an AI partial response with transactions, show it too
        if response_text:
             try:
                 await update.message.reply_text(response_text)
             except Exception:
                 pass
                 
        for tx_data in created_transactions:
            await show_transaction_with_actions(update, user_id, tx_data)


async def show_statistics(update: Update, api: MidasAPIClient, lang: str):
    """Show user statistics."""
    try:
        balance = await api.get_balance(period="month")
        breakdown = await api.get_category_breakdown(period="month")
        
        # Format statistics
        stats_text = get_message(lang, 'stats_month')
        
        # Extract categories list
        if breakdown and isinstance(breakdown, dict):
            categories = breakdown.get('categories', [])
            total_expense = float(breakdown.get('total_expense', 0))
            
            if categories:
                stats_text += get_message(lang, 'by_categories')
                
                # Filter out zero amounts and sort by amount desc
                valid_cats = [c for c in categories if float(c.get('total', 0)) > 0]
                valid_cats.sort(key=lambda x: float(x.get('total', 0)), reverse=True)
                
                for cat in valid_cats[:7]:  # Top 7
                    # Get name, prefer 'name' then 'category' (slug)
                    cat_name = cat.get('name') or cat.get('category') or get_message(lang, 'other')
                    if isinstance(cat_name, str):
                         cat_name = cat_name.title()
                         
                    cat_total = float(cat.get('total', 0))
                    
                    # Calculate percentage
                    percentage = 0
                    if total_expense > 0:
                        percentage = (cat_total / total_expense) * 100
                    
                    # Format: • Food: 50,000 (25%)
                    stats_text += f"• {cat_name}: {cat_total:,.0f} ({percentage:.1f}%)\n"
                
                stats_text += f"\n{get_message(lang, 'total')}: {total_expense:,.0f} {balance.get('currency', 'UZS')}"
            else:
                stats_text += "🤷‍♂️ No expenses yet this month."
        
        await update.message.reply_text(
            stats_text,
            reply_markup=get_main_keyboard(lang)
        )
    except Exception as e:
        logger.exception(f"Statistics error: {e}")
        await update.message.reply_text(
            get_message(lang, 'stats_error'), 
            reply_markup=get_main_keyboard(lang)
        )

async def show_balance(update: Update, api: MidasAPIClient, lang: str):
    """Show user balance."""
    try:
        balance_data = await api.get_balance()
        balance_value = float(balance_data.get('balance', 0))
        currency = balance_data.get('currency', 'UZS')
        
        balance_text = f"{get_message(lang, 'balance_month')}"
        balance_text += f"💰 {get_message(lang, 'your_balance')}: {balance_value:,.0f} {currency}\n\n"
        
        # Add recent transactions
        try:
            transactions_data = await api.get_transactions(limit=5)
            # Handle paginated response if it comes as dict with 'items' or list
            if isinstance(transactions_data, dict) and 'items' in transactions_data:
                transactions = transactions_data['items']
            elif isinstance(transactions_data, list):
                transactions = transactions_data
            else:
                transactions = []

            if transactions:
                balance_text += get_message(lang, 'last_transactions') + "\n"
                for tx in transactions:
                    icon = "📈" if tx['type'] == 'income' else "📉"
                    amount = float(tx['amount'])
                    desc = tx.get('description', '') or tx.get('category', {}).get('name', 'Transaction')
                    if isinstance(desc, dict): # if category is dict
                         desc = desc.get('name', '')
                         
                    # Format: 📉 50,000 - Lunch
                    balance_text += f"{icon} {amount:,.0f} - {desc}\n"
        except Exception as e:
            logger.error(f"Failed to fetch recent transactions: {e}")

        await update.message.reply_text(
            balance_text,
            reply_markup=get_main_keyboard(lang)
        )
    except Exception as e:
        logger.exception(f"Balance error: {e}")
        await update.message.reply_text(
            get_message(lang, 'error_occurred'),
            reply_markup=get_main_keyboard(lang)
        )
