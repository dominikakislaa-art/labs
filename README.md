# Лабораторные работы №1–9

**Студент:** Кислая Д.А. · **Номер задачи:** 14

Репозиторий: <https://github.com/dominikakislaa-art/labs>

Каждая работа — в отдельной папке, внутри плоская структура: код, тесты и `README.md` без лишних вложенных каталогов.

| Лаба | Задача №14 | Файлы | Запуск |
|---|---|---|---|
| [lab1](lab1/README.md) | Корзина интернет-магазина: структурный и ООП-стили | `structural.py`, `oop.py`, `README.md` | `python structural.py`, `python oop.py` |
| [lab2](lab2/README.md) | Сервис доставки еды: Scrum, Kanban, XP | `README.md`, `board.md` | — (документация) |
| [lab3](lab3/README.md) | Корзина: юнит-тесты и покрытие | `main.py`, `test_main.py`, `README.md` | `python -m pytest -q` |
| [lab4](lab4/README.md) | Подсчёт слов: юнит-тесты и BDD | `main.py`, `test_main.py`, `test_bdd.py`, `word_count.feature`, `README.md` | `python -m pytest -q` |
| [lab5](lab5/README.md) | Карта этажей: ветки, merge-конфликт, remote | `floor-map.md`, `README.md`, `.git` | `git log --oneline --graph --all` |
| [lab6](lab6/README.md) | Генератор номеров студбилетов: CI/CD | `ticket.py`, `test_ticket.py`, `.github/workflows/ci.yml`, `requirements.txt`, `README.md` | `python -m pytest -q` |
| [lab7](lab7/README.md) | Доставка еды: статусы заказа в Docker Compose | `api.py`, `Dockerfile`, `compose.yaml`, `README.md` | `docker compose up --build` |
| [lab8](lab8/README.md) | Доставка еды: документация и OpenAPI | `README.md`, `user.md`, `tech.md`, `openapi.yaml` | Swagger Editor / `python -m http.server` |
| [lab9](lab9/README.md) | Статусы заказа: код, тесты, AI-ревью | `order_status.py`, `test_order_status.py`, `README.md` | `python -m pytest -q` |

## Результаты тестов

| Лаба | Тесты |
|---|---|
| lab3 | 12 passed, покрытие `main.py` — 100 % |
| lab4 | 14 passed (10 юнит + 4 BDD) |
| lab6 | 16 passed |
| lab9 | 18 passed |
| lab7 | smoke-тест API (создание, статусы, отмена, ошибки) |

## Пояснения

- `lab5/.git` — обязательная часть работы №5: история веток, конфликт и слияния. Эта история также опубликована ветками `lab5/main`, `lab5/renumber-rooms`, `lab5/add-labs`. Учебный remote `lab5-origin.git` вынесен в `D:\Desktop\lab5-origin.git`, чтобы не засорять папку сдачи.
- `lab6/.github/workflows/ci.yml` — обязательная часть работы №6: конфигурация CI/CD лежит в репозитории.
- Зависимости ставятся командой из README каждой лабы (`pip install pytest ...`); `requirements.txt` оставлен только в lab6 — его использует CI.
- Docker в среде не установлен, поэтому lab7 проверена smoke-тестом API с `fakeredis`; `compose.yaml` провалидирован как YAML.
