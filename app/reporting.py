from __future__ import annotations

from collections import defaultdict
from typing import Dict, Any, Tuple

import pendulum as p

from .logging_utils import get_logger

log = get_logger(__name__)


def parse_period(natural: str | None) -> Tuple[p.DateTime, p.DateTime, str]:
    now = p.now()
    text = (natural or "").lower()
    log.info(f"period:parse input='{text}'")
    if not text or text.strip() == "":
        return now.subtract(days=30), now, "последние 30 дней"

    if "недел" in text:
        return now.subtract(days=7), now, "последнюю неделю"
    if "месяц" in text:
        return now.subtract(days=30), now, "последний месяц"
    if "вчера" in text:
        start = now.start_of("day").subtract(days=1)
        end = now.start_of("day")
        return start, end, "вчера"
    if "сегодня" in text:
        start = now.start_of("day")
        return start, now, "сегодня"

    # explicit dates like 2025-10-01 .. 2025-10-22
    import re

    m = re.findall(r"(\d{4}-\d{2}-\d{2})", text)
    if len(m) >= 1:
        start = p.parse(m[0]).start_of("day")
        end = p.parse(m[1]).end_of("day") if len(m) >= 2 else now
        label = f"с {start.to_date_string()} по {end.to_date_string()}"
        return start, end, label

    # fallback: last N days
    m2 = re.search(r"последн\w*\s+(\d+)\s+дн", text)
    if m2:
        days = int(m2.group(1))
        return now.subtract(days=days), now, f"последние {days} дней"

    return now.subtract(days=30), now, "последние 30 дней"


def summarize(expenses: list[dict[str, Any]]) -> Dict[str, Any]:
    by_cat = defaultdict(float)
    total = 0.0
    currency = None
    for e in expenses:
        amt = float(e["amount"])
        by_cat[e["category"]] += amt
        total += amt
        currency = currency or e.get("currency", "uzs")
    items = sorted(by_cat.items(), key=lambda kv: kv[1], reverse=True)
    log.info(f"summary:items={len(items)} total={total}")
    return {"items": items, "total": total, "currency": currency or "uzs"}


def format_report(summary: Dict[str, Any], label: str) -> str:
    lines = [f"Отчет за {label}:"]
    for cat, amt in summary["items"]:
        lines.append(f"- {cat}: {amt:.2f} {summary['currency']}")
    lines.append(f"Итого: {summary['total']:.2f} {summary['currency']}")
    return "\n".join(lines)
