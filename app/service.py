from cache.exact_cache import ExactMatchCache
from models.llm import MockLLM


class SmartLLMCacheService:
    """Checks cache first, then falls back to the LLM on a cache miss."""

    def __init__(self) -> None:
        self.exact_cache = ExactMatchCache()
        self.llm = MockLLM()

    def ask(self, query: str) -> dict:
        cache_result = self.exact_cache.get(query)

        if cache_result.hit:
            return {
                "response": cache_result.response,
                "source": "exact_cache",
                "tokens_generated": 0,
                "tokens_saved": cache_result.tokens_saved,
                "cache_latency_ms": round(cache_result.latency_ms, 2),
            }

        response, tokens_generated = self.llm.generate(query)

        self.exact_cache.set(
            query=query,
            response=response,
            tokens_generated=tokens_generated,
        )

        return {
            "response": response,
            "source": "llm",
            "tokens_generated": tokens_generated,
            "tokens_saved": 0,
            "cache_latency_ms": round(cache_result.latency_ms, 2),
        }