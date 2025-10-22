from __future__ import annotations

from typing import Optional, Dict, Any

import orjson
import redis

from .logging_utils import get_logger

log = get_logger(__name__)


class StateStore:
    def __init__(self, redis_url: str):
        self._r = redis.Redis.from_url(redis_url, decode_responses=False)
        self._ttl_seconds = 900  # 15 min

    def _key(self, user_id: str) -> str:
        return f"pending:{user_id}"

    def set_pending(self, user_id: str, payload: Dict[str, Any]) -> None:
        log.info(f"state:set user={user_id}")
        data = orjson.dumps(payload)
        self._r.setex(self._key(user_id), self._ttl_seconds, data)

    def get_pending(self, user_id: str) -> Optional[Dict[str, Any]]:
        log.info(f"state:get user={user_id}")
        raw = self._r.get(self._key(user_id))
        if not raw:
            return None
        try:
            return orjson.loads(raw)
        except Exception:
            log.exception("state:get decode error")
            return None

    def clear(self, user_id: str) -> None:
        log.info(f"state:clear user={user_id}")
        self._r.delete(self._key(user_id))

    def ping(self) -> bool:
        try:
            return bool(self._r.ping())
        except Exception:
            return False
