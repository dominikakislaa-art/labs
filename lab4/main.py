import re
from collections import Counter

SEPARATORS = re.compile(r"[\s,.!?;:]+")


def tokenize(text: str) -> list[str]:
    return [word for word in SEPARATORS.split(text.lower()) if word]


def word_count(text: str) -> int:
    return len(tokenize(text))


def top_word(text: str) -> str | None:
    words = tokenize(text)
    if not words:
        return None
    counts = Counter(words)
    return min(counts, key=lambda word: (-counts[word], word))
