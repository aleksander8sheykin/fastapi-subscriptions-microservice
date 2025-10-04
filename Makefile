export BUILDKIT_PROGRESS=plain
.PHONY: $(MAKECMDGOALS)
%:
	@:


DOCKER_IMAGE=subscriptions-service
COMPOSE_DEV=docker compose


# =====================
# ПОМОЩЬ
# =====================
help:
	@echo "===== Команды для локальной разработки ====="
	@echo "make test            - Запуск интеграционных тестов"
	@echo "make coverage        - Отчет о покрытии кода тестами"
	@echo "make lint-format     - Отформатировать код"
	@echo "make lint-check      - Проверить код"
	@echo ""
	@echo "===== Работа с Docker ====="
	@echo "make up              - Поднять docker-compose"
	@echo "make down            - Остановить все контейнеры"
	@echo "make rebuild         - Пересобрать все контейнеры"
	@echo "make restart         - Рестартануть все контейнеры"
	@echo "make logs            - Просмотр логов API"
	@echo "make build-prod TAG=0.1.8  - Сборка прод-образа с нужным тегом"
	@echo "make push-prod TAG=0.1.8   - Публикация прод-образа с нужным тегом"
	@echo ""
	@echo "===== Миграции ====="
	@echo "make create-migrations-file [FILENAME] - Создать файл миграции"
	@echo "make migrate-up         - Накатить все миграции"
	@echo "make migrate-down       - Откатить последнюю миграцию"
	@echo "make migrate-force v=3  - Проставить версию миграции"
	@echo "make migrate-goto v=5   - Перейти к миграции №5"

up:
	$(COMPOSE_DEV) up -d

down:
	$(COMPOSE_DEV) down

rebuild:
	$(COMPOSE_DEV) build

restart: down up

build-prod:
	docker build -t $(DOCKER_IMAGE):$(TAG) .

push-prod:
	docker push $(DOCKER_IMAGE):$(TAG)

logs:
	$(COMPOSE_DEV) logs -f app

make-migrations:
	$(COMPOSE_DEV) run --rm migrate alembic revision --autogenerate
	 
migrate-up:
	$(COMPOSE_DEV) run --rm migrate alembic upgrade head

migrate-down:
	$(COMPOSE_DEV) run --rm migrate alembic downgrade -1

test:
	$(COMPOSE_DEV) run --rm app-test bash -c "python -m pytest tests/"

coverage:
	$(COMPOSE_DEV) run --rm app-test python -m pytest --cov=app --cov-report=term-missing

lint-check:
	$(COMPOSE_DEV) run --rm app-test ruff check

lint-format:
	$(COMPOSE_DEV) run --rm app-test ruff check --fix