# Задача 14. Корзина интернет-магазина

**Студент:** Кислая Д.А.

---

## Постановка задачи

### 14. Корзина интернет-магазина

Напишите тесты и измерьте покрытие для модуля ниже.

```python
# main.py
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
```

### Общие требования

- Язык реализации тестов: **Python 3**.
- Тестируемый код — только функции из выданного `main.py`, без изменения их публичного поведения.
- Разрешены `pytest`, `unittest`, `coverage`, `pytest-cov`; сторонних библиотек в `main.py` нет.
- Тесты проверяют не только «счастливый путь», но и граничные случаи, ошибки и исключения.
- Имена тестов и структура файлов читаемые (`test_*.py`).
- В `README.md` указаны фамилия и инициалы и номер задачи.

---

## Структура репозитория

```
lab3/
├── main.py          # выданный модуль (без изменений поведения)
├── test_main.py     # 12 юнит-тестов
└── README.md
```

## Установка зависимостей

```bash
python -m pip install pytest pytest-cov
```

## Как запустить тесты

```bash
cd lab3
python -m pytest -q
```

Ожидаемый результат: `12 passed`.

## Как получить отчёт о покрытии

```bash
cd lab3
python -m pytest --cov=main --cov-report=term-missing
```

Можно добавить HTML-отчёт:

```bash
python -m pytest --cov=main --cov-report=html
# открыть htmlcov/index.html
```

### Результат прогона

```
Name      Stmts   Miss  Cover   Missing
---------------------------------------
main.py      23      0   100%
---------------------------------------
TOTAL        23      0   100%
12 passed
```

Покрытие строк `main.py` — **100 %**, все ветви условий (`price < 0`, `qty <= 0`, наличие/отсутствие позиции) выполнены.

---

## Что проверяется

| Функция | Тесты | Что покрыто |
|---------|-------|-------------|
| `add_or_update` | 4 | новая позиция; цена 0; повторное добавление (количество суммируется, цена обновляется); отрицательная цена и количество ≤ 0 → `ValueError` |
| `remove_item` | 1 | удаление существующей позиции (`True`), повторное удаление (`False`), корзина пуста |
| `cart_total` / `unique_count` | 1 | сумма `цена × количество`, пустая корзина → `0`, число позиций |
| `set_quantity` | 3 | установка положительного количества; `0` и отрицательное удаляют позицию; отсутствующая позиция → `KeyError` |

Граничные случаи, которые специально зафиксированы тестами:

- `price == 0` допустима (бесплатная позиция), `price < 0` — ошибка;
- `qty == 0` при добавлении — ошибка, а при `set_quantity` — удаление позиции;
- повторное `add_or_update` для существующего названия увеличивает количество и заменяет цену;
- `cart_total` на пустой корзине возвращает `0`, а не падает;
- `set_quantity` для отсутствующей позиции кидает `KeyError`, а не `ValueError` (так задано в модуле).

## Примечание

`main.py` скопирован из постановки без изменения публичного поведения: сигнатуры, возвращаемые значения и тексты исключений совпадают. Запуск `python -m pytest` из папки `lab3` подхватывает `main.py` без дополнительных настроек.
