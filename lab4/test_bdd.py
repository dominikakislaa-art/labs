from pytest_bdd import given, parsers, scenarios, then, when

from main import tokenize, top_word, word_count

scenarios("word_count.feature")


@given("пустой текст", target_fixture="ctx")
def empty_text():
    return {"text": ""}


@given(parsers.parse('текст "{text}"'), target_fixture="ctx")
def text_value(text):
    return {"text": text}


@when("я считаю количество слов", target_fixture="result")
def count_words(ctx):
    return word_count(ctx["text"])


@when("я разбиваю текст на слова", target_fixture="result")
def split_words(ctx):
    return tokenize(ctx["text"])


@when("я ищу самое частое слово", target_fixture="result")
def most_frequent(ctx):
    return top_word(ctx["text"])


@then(parsers.parse("количество слов равно {expected:d}"))
def check_count(ctx, expected):
    assert word_count(ctx["text"]) == expected


@then(parsers.parse('получаю слова "{expected}"'))
def check_tokens(result, expected):
    assert result == [word.strip() for word in expected.split(",")]


@then("самое частое слово отсутствует")
def check_none(ctx):
    assert top_word(ctx["text"]) is None


@then(parsers.parse('самое частое слово "{expected}"'))
def check_top_word(result, expected):
    assert result == expected
