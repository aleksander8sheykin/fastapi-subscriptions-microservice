

# Сервис подписок

Сервис управления онлайн-подписками пользователей. Написан на Python, использует Fastapi, SQLAlchemy, Pydantic, Alembic, Uvicorn и Docker.

## Особенности конфигурации

Нужно скопировать файл `.env.dev` в `.env`

Файл `.env.example` используется только как пример для Docker Compose.

## Makefile команды
###  Команды для локальной разработки
- `make test`            - Запуск интеграционных тестов
- `make coverage`        - Отчет о покрытии кода тестами

### Работа с Docker
- `make up`              - Поднять docker-compose
- `make down`            - Остановить все контейнеры
- `make build`           - Пересобрать базовый образ
- `make restart`         - Рестартануть все контейнеры
- `make logs`            - Просмотр логов API
- `make build-prod TAG=0.1.8`   - Сборка прод-образа с нужным тегом
- `make push-prod TAG=0.1.8`    - Публикация прод-образа с нужным тегом
- `make run-prod TAG=0.1.8`     - Запуск прод-образа с нужным тегом локально"

### Миграции
- `make migrate`         - Накатить все миграции
- `make migrate-down`    - Откатить миграцию на 1 шаг   

## Как запустить дев окружение
1.  Скопировать файл `.env.dev` в `.env`
2. `make up`

Сервис будет доступен на http://localhost:8080/

http://localhost:8080/docs - Swagger документация

http://localhost:8080/subscriptions - Ручки проекта


## Как запустить собранный прод-образ локально

```
make run-prod TAG=0.0.1
```
Запустит прод образ на порту `:8081`
Обращения будут идти в дев базу

### Запуск тестов

В проекте представлены только интеграционные тесты, так как логика микросервиса
не подразумевает сложное деление кода и перепроверка каждого изолированного слоя
избыточна.

Интеграционные тесты используют базу проекта с постфиксом `_test`

- Интеграционные тесты:
```bash
make test
```

-  Отчёт покрытия:
```bash
make coverage
```

## Архитектура

Проект построен по feature-based подходу, где вся логика собрана по фичам, которы находятя в папке app

Фича `subscriptions` - отвечает за подписки

Внутри `app/subscriptions/` используется разделение по слоям:

- routes — голые ручки
- handlers — бизнес логика
- repository — работа с БД
- models — модели данных

`app/core` - Отвечает за общие модули между фичами

```
project-root/
│
├── app/                      # приложение
│   ├── core/                 # общие модули
│   │   ├── db.py             # engine, session, Base
│   │   └── logging.py        # настройка логирования (опционально)
│   │
│   ├── subscriptions/        # фича "подписки"
│   │   ├── handlers.py       # FastAPI хандлеры (бизнес логика)
│   │   ├── models.py         # SQLAlchemy модели
│   │   ├── schemas.py        # Pydantic схемы
│   │   ├── routes.py         # FastAPI роуты (эндпоинты)
│   │   └── respository.py    # Слой работы с базой
│   │
│   ├── main.py               # точка входа FastAPI
│   └── config.py             # Settings (чтение env vars)
│
├── migrations/               # каталог с миграциями и нстройками Alembic
│   ├── versions/             # файлы миграций
│   └── env.py                # конфиг Alembic (читает settings)
│
├── tests/                    # тесты (используют _test базу)
│   ├── conftest.py
│   └── test_subscriptions.py
│
├── .env                      # локальные переменные окружения (копия из .env.dev)
├── .env.dev                  # переменные окружения для dev
├── alembic.ini               # конфиг Alembic (лежит в корне!)
├── docker-compose.yml        # dev окружение (app, app-test, migrate, db)
├── Dockerfile                # мультистейдж для prod/dev/test
├── Makefile                  # команды для удобства (restart, test, migrate и т.п.)
├── pyproject.toml            # настройки форматеров кода
├── pytest.ini                # настройки тестов
├── README.md
├── requirements.txt          # зависимости
└── Subscriptions Service API.postman_collection.json  - Готовая коллекция запросов для Postman
```