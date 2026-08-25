import uuid
import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

logger = logging.getLogger(__name__)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware that ensures every API request has a correlation X-Request-ID header.
    Reuses incoming header if supplied, otherwise generates a UUID4.
    Logs request latency and method.
    """
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID") or uuid.uuid4().hex
        request.state.request_id = request_id

        start_time = time.time()
        response = await call_next(request)
        duration_ms = round((time.time() - start_time) * 1000, 2)

        response.headers["X-Request-ID"] = request_id
        logger.info(
            f"req_id={request_id} method={request.method} path={request.url.path} status={response.status_code} duration={duration_ms}ms"
        )
        return response
