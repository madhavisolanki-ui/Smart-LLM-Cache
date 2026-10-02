from cache.exact_cache import ExactMatchCache


def test_exact_cache_hit():
    cache = ExactMatchCache()

    cache.set(
        query="What is Python?",
        response="Python is a general-purpose programming language.",
        tokens_generated=8,
    )

    result = cache.get("What is Python?")

    assert result.hit is True
    assert result.response == "Python is a general-purpose programming language."
    assert result.tokens_saved == 8


def test_query_normalization():
    cache = ExactMatchCache()

    cache.set(
        query="What is Python?",
        response="Python is a programming language.",
        tokens_generated=6,
    )

    result = cache.get("  what    is PYTHON?  ")

    assert result.hit is True
    assert result.response == "Python is a programming language."


def test_cache_miss():
    cache = ExactMatchCache()

    result = cache.get("What is Java?")

    assert result.hit is False
    assert result.response is None
    assert result.tokens_saved == 0


def test_cache_size():
    cache = ExactMatchCache()

    cache.set("What is Python?", "Python is a language.", 5)
    cache.set("What is Java?", "Java is a language.", 5)

    assert cache.size() == 2