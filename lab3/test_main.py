import pytest

from main import add_or_update, cart_total, remove_item, set_quantity, unique_count


def test_add_new_item():
    cart = {}
    add_or_update(cart, "Молоко", 2.5, 2)
    assert cart == {"Молоко": {"price": 2.5, "qty": 2}}


def test_add_existing_updates_price_and_qty():
    cart = {"Молоко": {"price": 2.5, "qty": 2}}
    add_or_update(cart, "Молоко", 3.0, 1)
    assert cart["Молоко"] == {"price": 3.0, "qty": 3}


def test_add_zero_price_allowed():
    cart = {}
    add_or_update(cart, "Пробник", 0, 1)
    assert cart_total(cart) == 0


@pytest.mark.parametrize("price,qty", [(-1, 1), (1, 0), (1, -1)])
def test_add_invalid_values(price, qty):
    with pytest.raises(ValueError):
        add_or_update({}, "Сыр", price, qty)


def test_remove_item():
    cart = {"Хлеб": {"price": 1, "qty": 1}}
    assert remove_item(cart, "Хлеб") is True
    assert remove_item(cart, "Хлеб") is False
    assert cart == {}


def test_total_and_count():
    cart = {"Молоко": {"price": 2.5, "qty": 2}, "Хлеб": {"price": 1, "qty": 3}}
    assert cart_total(cart) == 8
    assert unique_count(cart) == 2
    assert cart_total({}) == 0


def test_set_quantity():
    cart = {"Хлеб": {"price": 1, "qty": 1}}
    set_quantity(cart, "Хлеб", 5)
    assert cart["Хлеб"]["qty"] == 5


@pytest.mark.parametrize("qty", [0, -2])
def test_set_quantity_zero_or_less_deletes(qty):
    cart = {"Хлеб": {"price": 1, "qty": 1}}
    set_quantity(cart, "Хлеб", qty)
    assert cart == {}


def test_set_quantity_missing_item():
    with pytest.raises(KeyError):
        set_quantity({}, "Кефир", 1)
