FROM python:3.12-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/

RUN pip install --upgrade pip && \
    pip install --user -r requirements.txt

FROM python:3.12-slim

WORKDIR /app

# Настроим PATH для пакетов, установленных с --user
ENV PATH=/root/.local/bin:$PATH

# Копируем установленные пакеты и код приложения
COPY --from=builder /root/.local /root/.local
COPY ./app /app/app
COPY ./migrations /app/migrations
COPY ./alembic.ini /app/

# Команда по умолчанию
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]