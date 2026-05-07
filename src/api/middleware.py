import uuid
from collections.abc import Awaitable, Callable

import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class CorrelationIdMMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add a unique correlation ID to each request for better traceability in logs.
    """
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        correlation_id = request.headers.get("x-correlation-id") or str(uuid.uuid4())
        structlog.contextvars.bind_contextvars(correlation_id=correlation_id)
        try:
            response: Response = await call_next(request)
            response.headers["x-correlation-id"] = correlation_id
            return response
        finally:
            structlog.contextvars.clear_contextvars()