**MiuMiu Clean**

Краткое описание
: Лёгкий CRUD-сервис для управления категориями, продуктами и заказами, реализованный на FastAPI.

**Project Structure**
- **app/**: основной пакет приложения (API, domain, инфраструктура).
- **app/api/routers/**: маршруты API (`categories.py`, `products.py`, `orders.py`).
- **app/infrastructure/db/**: модели и сессия БД.
- **app/use_cases/**: бизнес-логика (сервисы для категорий, продуктов и заказов).

**Требования**
- Python 3.10+
- Зависимости перечислены в `requirements.txt`.

**Установка**

1. Клонируйте репозиторий и перейдите в папку проекта:

```bash
git clone https://github.com/nicetea9/miumiu_shop.git
cd miumiu_clean
```

**Docker**

1. Собрать образ и запустить через docker-compose:

```bash
docker compose build
docker compose up
```

2. Контейнеры описаны в `docker-compose.yml` и `Dockerfile`.

**API Endpoints (основные)**
- `GET /categories` — список категорий
- `POST /categories` — создать категорию
- `GET /products` — список продуктов
- `POST /products` — создать продукт
- `GET /orders` — список заказов
- `POST /orders` — создать заказ

Примеры curl:

```bash
curl -X GET http://127.0.0.1:8000/categories

curl -X POST http://127.0.0.1:8000/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Product A","category_id":1,"price":100.0}'
```

**Тестирование**

Запуск тестов (pytest):

```bash
python3 -m pip install -r requirements.txt
python3 -m pytest --cov=app --cov-report=term-missing -v
```

**Разработка**
- Бизнес-логика находится в `app/use_cases/`.
- Репозитории и слои доступа к данным — в `app/infrastructure/repositories` и `app/infrastructure/db`.
- Точки входа для API — в `app/api/routers/`.

**Полезные команды**
- Установить зависимости: `pip install -r requirements.txt`
- Запуск dev-сервера: `uvicorn app.main:app --reload`
- Сборка контейнера: `docker compose build`
- Запуск контейнеров: `docker compose up`
