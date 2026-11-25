import pytest

from main import tokenize, top_word, word_count


def test_tokenize_lowercases_and_strips_punctuation():
    assert tokenize("Привет, МИР!") == ["привет", "мир"]


def test_tokenize_splits_on_all_separators():
    assert tokenize("a,b.c!d?e;f:g\th\ni") == list("abcdefghi")


def test_tokenize_empty_and_punctuation_only():
    assert tokenize("") == []
    assert tokenize(" ,.!?;: ") == []


def test_word_count():
    assert word_count("") == 0
    assert word_count("один два, три!") == 3


def test_top_word_clear_winner():
    assert top_word("кот кот кот пёс") == "кот"


def test_top_word_tie_returns_smallest():
    assert top_word("яблоко банан яблоко банан") == "банан"


def test_top_word_empty():
    assert top_word("") is None


def test_top_word_lowercases():
    assert top_word("Слово") == "слово"


@pytest.mark.parametrize("text", ["...", "   "])
def test_top_word_only_separators(text):
    assert top_word(text) is None
