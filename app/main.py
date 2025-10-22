from __future__ import annotations

import os
from typing import Optional, List

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from .config import get_settings
from .state import StateStore
from .ai import parse_expense, transcribe_ogg_bytes, check_openai, ai_generate_report
from .storage import ExpenseStore
from .reporting import parse_period, summarize, format_report
from .categories import list_categories
from .logging_utils import configure_logging, get_logger
from .i18n import t, preview


settings = get_settings()
configure_logging("INFO")
log = get_logger(__name__)

BOT = telebot.TeleBot(settings.telegram_bot_token, parse_mode="HTML")
state = StateStore(settings.redis_url)
store = ExpenseStore(settings.supabase_url, settings.supabase_anon_key)


LANG_CHOICES = [("ru", "Русский"), ("en", "English")]
CURR_CHOICES = ["uzs", "usd", "eur", "rub"]


def _user_id(msg) -> str:
    return str(msg.from_user.id)


def _kb_lang() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    kb.row(*[InlineKeyboardButton(text=label, callback_data=f"setlang:{code}") for code, label in LANG_CHOICES])
    return kb


def _kb_currency() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    kb.row(*[InlineKeyboardButton(text=c.upper(), callback_data=f"setcur:{c}") for c in CURR_CHOICES])
    return kb


def _render_preview(d: dict, lang: str) -> str:
    cat = d.get("category_slug") or "other"
    conf = d.get("category_confidence", 0.0)
    return preview(lang, d.get("description"), float(d["amount"]), d.get("currency"), cat, float(conf))


def _get_lang_currency(user_id: str) -> tuple[str, str]:
    s = store.get_user_settings(user_id)
    lang = (s.get("language") or "ru").lower()
    currency = (s.get("currency") or settings.default_currency).lower()
    return lang, currency


@BOT.message_handler(commands=["start"]) 
def cmd_start(msg):
    user = _user_id(msg)
    s = store.get_user_settings(user)
    lang = (s.get("language") or "").lower()
    if not lang:
        BOT.reply_to(msg, t("ru", "start_choose_lang"), reply_markup=_kb_lang())
        return
    _send_start_info(msg, lang)


def _send_start_info(msg, lang: str):
    cats = ", ".join(list_categories())
    _, currency = _get_lang_currency(_user_id(msg))
    BOT.reply_to(msg, t(lang, "start", cats=cats, currency=currency))
    if not _get_lang_currency(_user_id(msg))[1]:
        BOT.send_message(msg.chat.id, t(lang, "choose_currency"), reply_markup=_kb_currency())


@BOT.callback_query_handler(func=lambda c: c.data.startswith("setlang:"))
def cb_setlang(call: CallbackQuery):
    lang = call.data.split(":", 1)[1]
    user = str(call.from_user.id)
    store.upsert_user_settings(user, language=lang)
    BOT.answer_callback_query(call.id, text=f"Language: {lang}")
    BOT.send_message(call.message.chat.id, t(lang, "choose_currency"), reply_markup=_kb_currency())


@BOT.callback_query_handler(func=lambda c: c.data.startswith("setcur:"))
def cb_setcur(call: CallbackQuery):
    cur = call.data.split(":", 1)[1]
    user = str(call.from_user.id)
    s = store.get_user_settings(user)
    lang = (s.get("language") or "ru").lower()
    store.upsert_user_settings(user, currency=cur)
    BOT.answer_callback_query(call.id, text=f"Currency: {cur}")
    _send_start_info(call.message, lang)


@BOT.message_handler(commands=["setlang"]) 
def cmd_setlang(msg):
    BOT.reply_to(msg, t("ru", "start_choose_lang"), reply_markup=_kb_lang())


@BOT.message_handler(commands=["setcurrency"]) 
def cmd_setcurrency(msg):
    lang, _ = _get_lang_currency(_user_id(msg))
    BOT.reply_to(msg, t(lang, "choose_currency"), reply_markup=_kb_currency())


@BOT.message_handler(commands=["health"]) 
def cmd_health(msg):
    oai_ok = check_openai(settings.openai_api_key)
    redis_ok = state.ping()
    supa_ok, supa_msg = store.ping_detail()
    lang, _ = _get_lang_currency(_user_id(msg))
    def mark(ok: bool) -> str:
        return "✅" if ok else "❌"
    text = (
        f"OpenAI: {mark(oai_ok)}\n"
        f"Redis: {mark(redis_ok)}\n"
        f"Supabase: {mark(supa_ok)}"
    )
    if not supa_ok:
        text += f"\n<code>{supa_msg}</code>"
    text += "\n" + (t(lang, "health_all_ok") if (oai_ok and redis_ok and supa_ok) else t(lang, "health_fix"))
    BOT.reply_to(msg, text)


def _chunk_send_text(chat_id: int, text: str, chunk_size: int = 3500) -> None:
    while text:
        chunk = text[:chunk_size]
        BOT.send_message(chat_id, chunk)
        text = text[chunk_size:]


@BOT.message_handler(commands=["report"])
def cmd_report(msg):
    text = msg.text or ""
    arg = text.partition(" ")[2].strip()
    start, end, label = parse_period(arg)
    user = _user_id(msg)
    lang, currency = _get_lang_currency(user)

    # default cap: last 30 days via parse_period fallback; fetch within [start, end]; no more than 1000 rows to AI
    data = store.fetch_expenses(user, start, end)
    data = data[-1000:]

    # prepare minimal records
    expenses = []
    for e in sorted(data, key=lambda x: x.get("expense_date")):
        expenses.append(
            {
                "amount": float(e.get("amount", 0)),
                "currency": (e.get("currency") or currency).lower(),
                "category": e.get("category"),
                "description": e.get("description"),
                "expense_date": e.get("expense_date"),
            }
        )

    try:
        reply = ai_generate_report(settings.openai_api_key, arg or ("report" if lang == "en" else "сделай отчет"), label, expenses)
        if not reply:
            reply = ("No data or unknown request." if lang == "en" else "Похоже, данных нет или запрос не распознан.")
    except Exception:
        log.exception("report:ai error, fallback to summary")
        summary = summarize(data)
        reply = format_report(summary, label)

    _chunk_send_text(msg.chat.id, reply)


@BOT.message_handler(content_types=["voice"]) 
def on_voice(msg):
    user = _user_id(msg)
    lang, currency = _get_lang_currency(user)
    file_info = BOT.get_file(msg.voice.file_id)
    file_bytes = BOT.download_file(file_info.file_path)
    transcript = transcribe_ogg_bytes(file_bytes, settings.openai_api_key)
    parsed = parse_expense(transcript, settings.openai_api_key)
    parsed.setdefault("currency", currency)
    parsed.setdefault("description", transcript)
    state.set_pending(user, parsed)
    BOT.reply_to(msg, _render_preview(parsed, lang))


@BOT.message_handler(func=lambda m: True, content_types=["text"]) 
def on_text(msg):
    text = (msg.text or "").strip()
    user = _user_id(msg)
    lang, currency = _get_lang_currency(user)

    # Confirmation flow
    pending = state.get_pending(user)
    if pending:
        low = text.lower()
        if low in ("да", "ок", "+", "yes", "y"):
            store.insert_expense(
                user_id=user,
                amount=float(pending["amount"]),
                currency=pending.get("currency", currency),
                category=(pending.get("category_slug") or "other"),
                description=pending.get("description", ""),
            )
            state.clear(user)
            BOT.reply_to(msg, t(lang, "saved"))
            return
        if low in ("нет", "no", "n", "отмена"):
            state.clear(user)
            BOT.reply_to(msg, t(lang, "cancelled"))
            return
        # inline corrections
        if ":" in text:
            key, _, val = text.partition(":")
            key = key.strip().lower()
            val = val.strip()
            if key.startswith("катег") or key.startswith("categ"):
                pending["category_slug"] = val.lower()
            elif key.startswith("сумм") or key.startswith("amount"):
                try:
                    pending["amount"] = float(val.replace(",", "."))
                except Exception:
                    pass
            elif key.startswith("опис") or key.startswith("descr"):
                pending["description"] = val
            state.set_pending(user, pending)
            BOT.reply_to(msg, _render_preview(pending, lang))
            return

    # New parse
    parsed = parse_expense(text, settings.openai_api_key)
    parsed.setdefault("currency", currency)

    # If category is missing or confidence low, ask clarification
    if not parsed.get("category_slug") or float(parsed.get("category_confidence", 0.0)) < 0.5:
        state.set_pending(user, parsed)
        BOT.reply_to(
            msg,
            _render_preview(parsed, lang)
            + ("\n\n" + t(lang, "need_category")),
        )
        return

    state.set_pending(user, parsed)
    BOT.reply_to(msg, _render_preview(parsed, lang))


if __name__ == "__main__":
    BOT.infinity_polling(timeout=60, long_polling_timeout=40)
