import time
from typing import Any, Optional

class SimpleCache:
    def __init__(self):
        self._cache = {}

    def get(self, key: str) -> Optional[Any]:
        entry = self._cache.get(key)
        if entry:
            value, expires_at = entry
            if expires_at is None or expires_at > time.time():
                return value
            else:
                del self._cache[key]
        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        expires_at = time.time() + ttl if ttl else None
        self._cache[key] = (value, expires_at)

    def invalidate(self, key: str):
        if key in self._cache:
            del self._cache[key]

cache = SimpleCache() 