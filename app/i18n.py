from __future__ import annotations

from typing import Dict


_TEXTS: Dict[str, Dict[str, str]] = {
    "ru": {
        "start_choose_lang": "Выберите язык / Choose language:",
        "choose_currency": "Выберите валюту по умолчанию:",
        "start": (
            "Привет! Я бот-бухгалтер. Пиши о тратах текстом или голосом — я распаршу, "
            "попрошу подтвердить и сохраню. Команда /report для отчета.\n\n"
            "Категории: {cats}\nВалюта по умолчанию: {currency}"
        ),
        "saved": "Сохранил ✅",
        "cancelled": "Отменил. Отправь новую трату.",
        "need_category": "Нужна уточнение по категории. Укажи, пожалуйста (одно слово, напр. food/transport/...).",
        "report_no_data": "Нет трат за {label}.",
        "health_all_ok": "Все ок, можно работать.",
        "health_fix": "Проверь .env/сервисы.",
    },
    "en": {
        "start_choose_lang": "Choose language:",
        "choose_currency": "Choose default currency:",
        "start": (
            "Hi! I'm your accountant bot. Send expenses by text or voice — I'll parse, "
            "ask to confirm and save. Use /report for reports.\n\n"
            "Categories: {cats}\nDefault currency: {currency}"
        ),
        "saved": "Saved ✅",
        "cancelled": "Cancelled. Send a new expense.",
        "need_category": "Please specify a category (one word, e.g., food/transport/...).",
        "report_no_data": "No expenses for {label}.",
        "health_all_ok": "All good.",
        "health_fix": "Check .env/services.",
    },
}


def t(lang: str, key: str, **kwargs) -> str:
    lang = (lang or "ru").lower()
    if lang not in _TEXTS:
        lang = "en"
    txt = _TEXTS[lang].get(key, _TEXTS["en"].get(key, key))
    try:
        return txt.format(**kwargs)
    except Exception:
        return txt


def preview(lang: str, description: str, amount: float, currency: str, category: str, confidence: float) -> str:
    if (lang or "ru").lower().startswith("en"):
        return (
            f"Expense: {description or '—'}\n"
            f"Amount: <b>{amount:.2f} {currency}</b>\n"
            f"Category: <b>{category}</b> (confidence {confidence:.2f})\n\n"
            f"Reply: <b>yes</b>/<b>no</b> or correct via text."
        )
    return (
        f"Расходы: {description or '—'}\n"
        f"Сумма: <b>{amount:.2f} {currency}</b>\n"
        f"Категория: <b>{category}</b> (уверенность {confidence:.2f})\n\n"
        f"<b>да</b> / <b>нет</b> или исправьте текстом."
    )
