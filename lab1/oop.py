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


class Item:
    def __init__(self, name, price, qty):
        self._name, self._price, self._qty = name, price, qty

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    @property
    def qty(self):
        return self._qty

    @property
    def amount(self):
        return self._price * self._qty

    def add(self, price, qty):
        self._price = price
        self._qty += qty

    def set_qty(self, qty):
        self._qty = qty

    def __str__(self):
        return "%-12s %6.2f x %-3d = %8.2f" % (self._name, self._price,
                                               self._qty, self.amount)


class Cart:
    def __init__(self):
        self._items = {}

    def __len__(self):
        return len(self._items)

    @property
    def total(self):
        return sum(item.amount for item in self._items.values())

    def add(self, name, price, qty=1):
        text, price, qty = norm(name), float(price), int(qty)
        check_price(price)
        check_qty(qty)
        key = text.casefold()
        item = self._items.get(key)
        if item is None:
            self._items[key] = item = Item(text, price, qty)
        else:
            item.add(price, qty)
        return item

    def _key(self, name):
        key = norm(name).casefold()
        if key not in self._items:
            raise ValueError("Позиции «%s» нет в корзине" % name)
        return key

    def find(self, name):
        return self._items[self._key(name)]

    def set_qty(self, name, qty):
        qty = int(qty)
        check_qty(qty)
        self.find(name).set_qty(qty)

    def remove(self, name):
        return self._items.pop(self._key(name)).name

    def report(self):
        lines = ["Корзина: позиций %d, итого %.2f" % (len(self), self.total)]
        lines.extend("  %s" % item for item in self._items.values())
        return "\n".join(lines)


def demo():
    print("=== Задача 14. Корзина интернет-магазина ===")
    print("Стиль: объектно-ориентированный (классы Item и Cart)")
    print()

    cart = Cart()
    print("Добавляем: Молоко 2.50 x 2, Хлеб 1.20 x 1, Сыр 5.40 x 1")
    cart.add("Молоко", 2.50, 2)
    cart.add("Хлеб", 1.20)
    cart.add("Сыр", 5.40)
    print(cart.report())
    print()

    print("Добавляем ещё 1 Молоко по 2.80 (цена обновляется)")
    cart.add("молоко", 2.80)
    milk = cart.find("МОЛОКО")
    print("Молоко: %.2f x %d" % (milk.price, milk.qty))

    print("Меняем количество Хлеба на 4")
    cart.set_qty("хлеб", 4)

    print("Удаляем Сыр")
    print("Удалён: %s" % cart.remove("Сыр"))
    print()

    print("Позиций в корзине: %d" % len(cart))
    print(cart.report())
    print()

    checks = [
        ("Удаляем Кефир", lambda: cart.remove("Кефир")),
        ("Ставим Хлебу количество 0", lambda: cart.set_qty("Хлеб", 0)),
        ("Добавляем позицию без названия", lambda: cart.add("   ", 1.0)),
    ]
    for title, action in checks:
        try:
            action()
            print("%s -> ошибки не было" % title)
        except ValueError as error:
            print("%s -> Ошибка: %s" % (title, error))
    print()

    print("Итог: позиций %d, сумма %.2f" % (len(cart), cart.total))


if __name__ == "__main__":
    demo()
