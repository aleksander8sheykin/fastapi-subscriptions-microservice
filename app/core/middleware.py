import random

from fastapi import Request

from app.core.context import trace_id_ctx
from app.core.logging import get_logger

logger = get_logger("app.middleware")


async def add_trace_id(request: Request, call_next):
    trace_id = random.randint(10**12, 10**13 - 1)
    trace_id_ctx.set(trace_id)
    logger.info("Incoming request %s %s", request.method, request.url.path)
    response = await call_next(request)
    return response
