from contextvars import ContextVar

trace_id_ctx: ContextVar[int | None] = ContextVar("trace_id", default=None)
