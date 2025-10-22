from __future__ import annotations

import io
from typing import Dict, Any, List

from openai import OpenAI

from .categories import CATEGORIES
from .logging_utils import get_logger

log = get_logger(__name__)


def _client(api_key: str) -> OpenAI:
    return OpenAI(api_key=api_key)


def transcribe_ogg_bytes(data: bytes, api_key: str) -> str:
    log.info("transcribe:start")
    client = _client(api_key)
    fileobj = io.BytesIO(data)
    fileobj.name = "audio.ogg"
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=("audio.ogg", fileobj, "audio/ogg"),
        response_format="text",
        temperature=0.0,
    )
    log.info("transcribe:done")
    return transcript


def parse_expense(text: str, api_key: str) -> Dict[str, Any]:
    log.info(f"parse_expense:start text_len={len(text)}")
    sys = (
        "Ты финансовый ассистент. Задача: извлечь расходы из коротких сообщений на русском. "
        "Верни ТОЛЬКО JSON с ключами: amount(number), currency(string), description(string), "
        "category_slug(string|null), category_confidence(number 0..1). Категории: "
        + ", ".join(CATEGORIES)
        + ". Если валюта не указана, поставь 'uzs'. Описание краткое."
    )
    user = f"Текст: {text}"

    client = _client(api_key)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": sys},
            {"role": "user", "content": user},
        ],
        temperature=0.0,
        response_format={"type": "json_object"},
    )

    import json, re

    try:
        data = json.loads(completion.choices[0].message.content)
        amount = float(data.get("amount", 0))
        currency = (data.get("currency") or "uzs").lower()
        description = (data.get("description") or "").strip()
        category_slug = data.get("category_slug")
        confidence = float(data.get("category_confidence", 0))
        log.info(f"parse_expense:ok amount={amount} currency={currency} category={category_slug} conf={confidence}")
        return {
            "amount": amount,
            "currency": currency,
            "description": description,
            "category_slug": category_slug,
            "category_confidence": confidence,
        }
    except Exception as e:
        log.exception("parse_expense:error")
        m = re.search(r"([0-9]+(?:[.,][0-9]{1,2})?)", text.replace(" ", ""))
        amount = float(m.group(1).replace(",", ".")) if m else 0.0
        return {
            "amount": amount,
            "currency": "uzs",
            "description": text.strip(),
            "category_slug": None,
            "category_confidence": 0.0,
        }


def check_openai(api_key: str) -> bool:
    try:
        client = _client(api_key)
        client.models.list()
        return True
    except Exception:
        return False


def ai_generate_report(api_key: str, query: str, label: str, expenses: List[Dict[str, Any]]) -> str:
    """Ask AI to interpret the report request and generate the answer.
    We provide structured expenses and a label; AI decides whether to summarize or list, and how.
    """
    log.info(f"report:ai start n={len(expenses)}")
    sys = (
        "Ты личный бухгалтер. Пользователь просит отчет о тратах. Тебе дан список расходов "
        "(массив объектов с полями amount, currency, category, description, expense_date). "
        "Если просит список — выведи понятный список с датами; если сводку — сгруппируй по категориям. "
        "Валюта выводится как есть (например, 'uzs'). Будь краток и по делу."
    )
    import json
    user_content = {
        "request": query,
        "period_label": label,
        "expenses": expenses,
    }
    client = _client(api_key)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": sys},
            {"role": "user", "content": json.dumps(user_content, ensure_ascii=False)},
        ],
        temperature=0.2,
    )
    text = completion.choices[0].message.content.strip()
    log.info("report:ai done")
    return text
