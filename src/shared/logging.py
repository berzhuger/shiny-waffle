import structlog
import logging

def configure_logging(level: str = "INFO", json_logs: bool = True):
    """
    Configures structlog for structured logging.
    """
    shared_processor = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
    ]

    if json_logs:
        processors = shared_processor + [structlog.processors.JSONRenderer()]
    else:
        processors = shared_processor + [structlog.dev.ConsoleRenderer()]

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(getattr(logging, level)),
        cache_logger_on_first_use=True,
        )

logger = structlog.get_logger()