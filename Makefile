export BUILDKIT_PROGRESS=plain
DOCKER_IMAGE := subscriptions-service
.PHONY: $(MAKECMDGOALS)

COMPOSE_DEV=docker compose

up:
	$(COMPOSE_DEV) up -d

down:
	$(COMPOSE_DEV) down

build:
	$(COMPOSE_DEV) build

restart: down up

build-prod:
	docker build -t $(DOCKER_IMAGE):$(TAG) .

push-prod:
	docker push $(DOCKER_IMAGE):$(TAG)

logs:
	$(COMPOSE_DEV) logs -f app

migrate:
	$(COMPOSE_DEV) run --rm migrate upgrade head

migrate-down:
	$(COMPOSE_DEV) run --rm migrate downgrade -1

test:
	$(COMPOSE_DEV) run --rm app-test sh -c "alembic upgrade head && python -m pytest tests/"

coverage:
	$(COMPOSE_DEV) run --rm app-test python -m pytest --cov=app --cov-report=term-missing
