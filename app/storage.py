from __future__ import annotations

from typing import Any, Dict, List, Tuple, Optional

import pendulum as p
from supabase import create_client, Client

from .logging_utils import get_logger

log = get_logger(__name__)


class ExpenseStore:
    def __init__(self, url: str, anon_key: str):
        self._client: Client = create_client(url, anon_key)

    def insert_expense(
        self,
        user_id: str,
        amount: float,
        currency: str,
        category: str,
        description: str,
        expense_date: str | None = None,
    ) -> None:
        log.info(f"supa:insert user={user_id} amt={amount} cur={currency} cat={category}")
        row = {
            "user_id": user_id,
            "amount": amount,
            "currency": currency,
            "category": category,
            "description": description,
        }
        if expense_date:
            row["expense_date"] = expense_date
        self._client.table("expenses").insert(row).execute()

    def fetch_expenses(self, user_id: str, start, end) -> List[Dict[str, Any]]:
        start_iso = p.instance(start).to_iso8601_string()
        end_iso = p.instance(end).to_iso8601_string()
        log.info(f"supa:fetch user={user_id} start={start_iso} end={end_iso}")
        res = (
            self._client.table("expenses")
            .select("user_id, amount, currency, category, description, expense_date")
            .eq("user_id", user_id)
            .gte("expense_date", start_iso)
            .lte("expense_date", end_iso)
            .execute()
        )
        return res.data or []

    def ping(self) -> bool:
        try:
            self._client.table("expenses").select("id").limit(1).execute()
            return True
        except Exception:
            return False

    def ping_detail(self) -> Tuple[bool, str]:
        try:
            self._client.table("expenses").select("id").limit(1).execute()
            return True, "ok"
        except Exception as e:
            log.exception("supa:ping error")
            return False, f"{type(e).__name__}: {e}"

    # User settings: language, currency
    def get_user_settings(self, user_id: str) -> Dict[str, Optional[str]]:
        try:
            res = (
                self._client.table("user_settings")
                .select("user_id, language, currency")
                .eq("user_id", user_id)
                .limit(1)
                .execute()
            )
            rows = res.data or []
            if rows:
                return {
                    "language": (rows[0].get("language") or "ru").lower(),
                    "currency": (rows[0].get("currency") or "uzs").lower(),
                }
        except Exception:
            log.exception("supa:get_user_settings error")
        return {"language": None, "currency": None}

    def upsert_user_settings(self, user_id: str, language: Optional[str] = None, currency: Optional[str] = None) -> None:
        payload: Dict[str, Any] = {"user_id": user_id}
        if language is not None:
            payload["language"] = language.lower()
        if currency is not None:
            payload["currency"] = currency.lower()
        log.info(f"supa:upsert_settings user={user_id} payload={payload}")
        self._client.table("user_settings").upsert(payload, on_conflict="user_id").execute()
