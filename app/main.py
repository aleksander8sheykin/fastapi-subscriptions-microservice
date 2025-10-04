from fastapi import FastAPI

from app.config import settings
from app.core.db import engine
from app.core.logging import get_logger, setup_logging
from app.core.middleware import add_trace_id
from app.subscriptions.routes import router as subscriptions_router

setup_logging(settings.LOG_LEVEL)
logger = get_logger(__name__)

app = FastAPI(
    title="Subscriptions Service",
    description="REST API для управления подписками пользователей",
    version="1.0.0",
)

app.middleware("http")(add_trace_id)

app.include_router(subscriptions_router, prefix="/subscriptions")


@app.get("/health", tags=["health"])
async def healthcheck():
    return {"status": "ok"}


@app.on_event("startup")
async def on_startup():
    logger.info("Application startup")


@app.on_event("shutdown")
async def on_shutdown():
    await engine.dispose()
    logger.info("Application shutdown")
