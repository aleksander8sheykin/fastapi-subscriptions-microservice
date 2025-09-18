# app/main.py
from fastapi import FastAPI

from app.config import settings
from app.core.logging import get_logger, setup_logging
from app.subscriptions.routes import router as subscriptions_router

setup_logging(settings.LOG_LEVEL)
logger = get_logger(__name__)

app = FastAPI(
    title="Subscriptions Service",
    description="REST API для управления подписками пользователей",
    version="1.0.0",
)

app.include_router(subscriptions_router, prefix="/subscriptions")


@app.get("/health", tags=["health"])
async def healthcheck():
    return {"status": "ok"}


@app.on_event("startup")
async def on_startup():
    logger.info("Application startup")


@app.on_event("shutdown")
async def on_shutdown():
    logger.info("Application shutdown")
