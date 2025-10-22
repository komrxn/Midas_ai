from __future__ import annotations

from typing import Tuple, Optional

CATEGORIES = [
    "food",
    "transport",
    "housing",
    "bills",
    "health",
    "shopping",
    "entertainment",
    "education",
    "travel",
    "family",
    "personal",
    "taxes_fees",
    "other",
]

# Russian keyword mapping to canonical slugs (broad/generalized)
SYNONYMS = {
    # food
    "продукт": "food",
    "супермаркет": "food",
    "магазин": "food",
    "еда": "food",
    "кофе": "food",
    "кафе": "food",
    "ресторан": "food",
    "столовая": "food",
    "доставка еды": "food",
    "фастфуд": "food",
    "пицц": "food",
    "суши": "food",
    # transport (includes fuel)
    "такси": "transport",
    "метро": "transport",
    "автобус": "transport",
    "трамвай": "transport",
    "маршрут": "transport",
    "каршеринг": "transport",
    "парков": "transport",
    "паркинг": "transport",
    "бензин": "transport",
    "заправ": "transport",
    # housing
    "аренда": "housing",
    "квартир": "housing",
    "ипотек": "housing",
    "ремонт": "housing",
    "мебел": "housing",
    # bills (utilities + internet + mobile)
    "коммунал": "bills",
    "жкх": "bills",
    "интернет": "bills",
    "связь": "bills",
    "мобил": "bills",
    "телефон": "bills",
    "электр": "bills",
    "вод": "bills",
    "газ": "bills",
    # health (includes pharmacy)
    "здоров": "health",
    "клиник": "health",
    "врач": "health",
    "стомат": "health",
    "анализ": "health",
    "апт": "health",
    # shopping (general goods incl. electronics)
    "покупк": "shopping",
    "одежд": "shopping",
    "обув": "shopping",
    "маркетплейс": "shopping",
    "бытов": "shopping",
    "техник": "shopping",
    "электро": "shopping",
    "гаджет": "shopping",
    # entertainment (incl. subscriptions)
    "кино": "entertainment",
    "развлеч": "entertainment",
    "игр": "entertainment",
    "подпис": "entertainment",
    "spotify": "entertainment",
    "netflix": "entertainment",
    # education
    "курс": "education",
    "обуч": "education",
    "учеб": "education",
    "книг": "education",
    # travel
    "поездк": "travel",
    "билет": "travel",
    "отел": "travel",
    "авиа": "travel",
    "виза": "travel",
    # family (kids, pets, gifts, donations)
    "дет": "family",
    "питом": "family",
    "зоо": "family",
    "корм": "family",
    "подар": "family",
    "донат": "family",
    "пожертв": "family",
    # personal (sport, beauty, care)
    "спорт": "personal",
    "фитнес": "personal",
    "салон": "personal",
    "красот": "personal",
    "космет": "personal",
    "уход": "personal",
    "барбер": "personal",
    # taxes & fees
    "налог": "taxes_fees",
    "комисс": "taxes_fees",
    "госпошлин": "taxes_fees",
    "пошлин": "taxes_fees",
    "сбор": "taxes_fees",
}


def list_categories() -> list[str]:
    return CATEGORIES.copy()


def normalize_slug(slug: str) -> Optional[str]:
    s = (slug or "").strip().lower()
    return s if s in CATEGORIES else None


def guess_category(text: str) -> Tuple[Optional[str], float]:
    t = (text or "").lower()
    best_slug: Optional[str] = None
    best_score: float = 0.0
    for key, slug in SYNONYMS.items():
        if key in t:
            score = min(1.0, 0.5 + 0.05 * len(key))
            if score > best_score:
                best_score = score
                best_slug = slug
    return best_slug, best_score
