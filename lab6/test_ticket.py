import pytest

from ticket import is_valid_number, make_number, next_number, parse_number


def test_make_number():
    assert make_number(2024, "ИТ", 42) == "24-09-0042-7"


def test_make_number_boundaries():
    assert make_number(2000, "ЭК", 1).startswith("00-38-0001-")
    assert make_number(2099, "МЕД", 9999).startswith("99-31-9999-")


@pytest.mark.parametrize(
    "year,faculty,seq",
    [(1999, "ИТ", 1), (2100, "ИТ", 1), (2024, "ФИЗ", 1), (2024, "ИТ", 0), (2024, "ИТ", 10000)],
)
def test_make_number_invalid(year, faculty, seq):
    with pytest.raises(ValueError):
        make_number(year, faculty, seq)


def test_parse_number():
    assert parse_number("24-09-0042-7") == {
        "year": 2024,
        "faculty": "ИТ",
        "seq": 42,
        "check": 7,
    }


@pytest.mark.parametrize(
    "number",
    ["24-09-0042", "24-09-0042-7-1", "aa-09-0042-7", "24-99-0042-7", "24-09-0000-7"],
)
def test_parse_number_invalid(number):
    with pytest.raises(ValueError):
        parse_number(number)


def test_is_valid_number():
    assert is_valid_number(make_number(2024, "ЮР", 7)) is True
    assert is_valid_number("24-09-0042-8") is False
    assert is_valid_number("мусор") is False


def test_next_number():
    assert next_number("24-09-0042-7") == make_number(2024, "ИТ", 43)


def test_next_number_exhausted():
    with pytest.raises(ValueError):
        next_number(make_number(2024, "ИТ", 9999))
