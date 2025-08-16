import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from .metrics import HTTP_REQUESTS_TOTAL, HTTP_REQUEST_DURATION


# Using BaseHTTPMiddleware for proper middleware handling
class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time

        endpoint = request.url.path
        method = request.method
        status = str(response.status_code)

        # Track request count
        HTTP_REQUESTS_TOTAL.labels(
            method=method,
            endpoint=endpoint,
            status=status
        ).inc()

        # Track latency with same labels
        HTTP_REQUEST_DURATION.labels(
            method=method,
            endpoint=endpoint,
            status=status
        ).observe(duration)

        return response
