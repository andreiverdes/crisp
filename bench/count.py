"""Text counting. words = whitespace split; tokens_est = tiktoken o200k_base (estimate)."""
from functools import lru_cache

TOKENIZER = "tiktoken/o200k_base"


@lru_cache(maxsize=1)
def _enc():
    import tiktoken

    return tiktoken.get_encoding("o200k_base")


def words(text: str) -> int:
    return len(text.split())


def tokens_est(text: str) -> int:
    return len(_enc().encode(text, disallowed_special=()))
