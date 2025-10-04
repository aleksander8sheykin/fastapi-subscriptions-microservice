import logging
import logging.config
import sys
from typing import Dict

from app.core.context import trace_id_ctx


class SingleLineFilter(logging.Filter):
    def filter(self, record):
        if isinstance(record.msg, str):
            record.msg = record.msg.replace("\n", "")
        trace_id = trace_id_ctx.get()
        record.trace_id = trace_id if trace_id is not None else 0
        return True


def setup_logging(level: str = "INFO") -> None:
    level = (level or "INFO").upper()

    config: Dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s %(levelname)s [%(name)s] [trace_id=%(trace_id)s] %(message)s",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "stream": "ext://sys.stdout",
                "filters": ["single_line_filter"],
            }
        },
        "filters": {
            "single_line_filter": {
                "()": SingleLineFilter,
            }
        },
        "root": {"level": level, "handlers": ["console"]},
        "loggers": {
            "app": {"level": level, "handlers": ["console"], "propagate": False},
            "uvicorn": {"level": "INFO", "handlers": ["console"], "propagate": False},
            "uvicorn.error": {
                "level": "ERROR",
                "handlers": ["console"],
                "propagate": False,
            },
            "uvicorn.access": {
                "level": "INFO",
                "handlers": ["console"],
                "propagate": False,
            },
            "sqlalchemy.engine": {
                "level": "INFO",
                "handlers": ["console"],
                "propagate": False,
            },
        },
    }

    logging.config.dictConfig(config)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


sys.modules.setdefault("app.core.logger", sys.modules[__name__])
