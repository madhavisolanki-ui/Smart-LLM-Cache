from app.service import SmartLLMCacheService


def test_second_identical_query_uses_cache():
    service = SmartLLMCacheService()

    first_result = service.ask("What is Python?")
    second_result = service.ask("What is Python?")

    assert first_result["source"] == "llm"
    assert first_result["tokens_generated"] > 0

    assert second_result["source"] == "exact_cache"
    assert second_result["tokens_generated"] == 0
    assert second_result["tokens_saved"] > 0

    assert first_result["response"] == second_result["response"]