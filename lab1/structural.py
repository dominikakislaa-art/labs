def norm(name):
    text = " ".join(str(name).split())
    if not text:
        raise ValueError("Название не может быть пустым")
    return text


def check_price(price):
    if price <= 0:
        raise ValueError("Цена должна быть больше 0")


def check_qty(qty):
    if qty <= 0:
        raise ValueError("Количество должно быть целым и больше 0")


def add(cart, name, price, qty=1):
    text, price, qty = norm(name), float(price), int(qty)
    check_price(price)
    check_qty(qty)
    key = text.casefold()
    item = cart.get(key)
    if item is None:
        cart[key] = item = {"name": text, "price": price, "qty": qty}
    else:
        item["price"], item["qty"] = price, item["qty"] + qty
    return item


def locate(cart, name):
    key = norm(name).casefold()
    if key not in cart:
        raise ValueError("Позиции «%s» нет в корзине" % name)
    return key


def find(cart, name):
    return cart[locate(cart, name)]


def set_qty(cart, name, qty):
    qty = int(qty)
    check_qty(qty)
    find(cart, name)["qty"] = qty


def remove(cart, name):
    return cart.pop(locate(cart, name))["name"]


def total(cart):
    return sum(item["price"] * item["qty"] for item in cart.values())


def count(cart):
    return len(cart)


def report(cart):
    lines = ["Корзина: позиций %d, итого %.2f" % (count(cart), total(cart))]
    for item in cart.values():
        lines.append("  %-12s %6.2f x %-3d = %8.2f"
                     % (item["name"], item["price"], item["qty"],
                        item["price"] * item["qty"]))
    return "\n".join(lines)


def demo():
    print("=== Задача 14. Корзина интернет-магазина ===")
    print("Стиль: структурный (функции + данные)")
    print()

    cart = {}
    print("Добавляем: Молоко 2.50 x 2, Хлеб 1.20 x 1, Сыр 5.40 x 1")
    add(cart, "Молоко", 2.50, 2)
    add(cart, "Хлеб", 1.20)
    add(cart, "Сыр", 5.40)
    print(report(cart))
    print()

    print("Добавляем ещё 1 Молоко по 2.80 (цена обновляется)")
    add(cart, "молоко", 2.80)
    milk = find(cart, "МОЛОКО")
    print("Молоко: %.2f x %d" % (milk["price"], milk["qty"]))

    print("Меняем количество Хлеба на 4")
    set_qty(cart, "хлеб", 4)

    print("Удаляем Сыр")
    print("Удалён: %s" % remove(cart, "Сыр"))
    print()

    print("Позиций в корзине: %d" % count(cart))
    print(report(cart))
    print()

    checks = [
        ("Удаляем Кефир", lambda: remove(cart, "Кефир")),
        ("Ставим Хлебу количество 0", lambda: set_qty(cart, "Хлеб", 0)),
        ("Добавляем позицию без названия", lambda: add(cart, "   ", 1.0)),
    ]
    for title, action in checks:
        try:
            action()
            print("%s -> ошибки не было" % title)
        except ValueError as error:
            print("%s -> Ошибка: %s" % (title, error))
    print()

    print("Итог: позиций %d, сумма %.2f" % (count(cart), total(cart)))


if __name__ == "__main__":
    demo()
