 
from dataclasses import dataclass
from hashlib import sha256
from time import perf_counter


@dataclass
class CacheResult:
    hit: bool
    response: str | None = None
    tokens_saved: int = 0
    latency_ms: float = 0.0


class ExactMatchCache:
    """In-memory cache for normalized, exact user queries."""

    def __init__(self) -> None:
        self._store: dict[str, dict[str, str | int]] = {}

    @staticmethod
    def _normalize(query: str) -> str:
        return " ".join(query.lower().strip().split())

    def _key(self, query: str) -> str:
        normalized_query = self._normalize(query)
        return sha256(normalized_query.encode("utf-8")).hexdigest()

    def get(self, query: str) -> CacheResult:
        start = perf_counter()
        entry = self._store.get(self._key(query))
        latency_ms = (perf_counter() - start) * 1000

        if entry is None:
            return CacheResult(hit=False, latency_ms=latency_ms)

        return CacheResult(
            hit=True,
            response=str(entry["response"]),
            tokens_saved=int(entry["tokens_generated"]),
            latency_ms=latency_ms,
        )

    def set(self, query: str, response: str, tokens_generated: int) -> None:
        self._store[self._key(query)] = {
            "query": self._normalize(query),
            "response": response,
            "tokens_generated": tokens_generated,
        }

    def size(self) -> int:
        return len(self._store)