from typing import Dict


def add_or_update(cart: Dict[str, dict], name: str, price: float, qty: int) -> None:
    if price < 0 or qty <= 0:
        raise ValueError("invalid price or qty")
    if name in cart:
        cart[name]["qty"] += qty
        cart[name]["price"] = price
    else:
        cart[name] = {"price": price, "qty": qty}


def remove_item(cart: Dict[str, dict], name: str) -> bool:
    if name in cart:
        del cart[name]
        return True
    return False


def cart_total(cart: Dict[str, dict]) -> float:
    return sum(item["price"] * item["qty"] for item in cart.values())


def unique_count(cart: Dict[str, dict]) -> int:
    return len(cart)


def set_quantity(cart: Dict[str, dict], name: str, qty: int) -> None:
    if name not in cart:
        raise KeyError("item not found")
    if qty <= 0:
        del cart[name]
    else:
        cart[name]["qty"] = qty
