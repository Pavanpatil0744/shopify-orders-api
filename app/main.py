import time
from fastapi import Request

from .metrics import HTTP_REQUESTS_TOTAL, HTTP_REQUEST_DURATION

@app.middleware("http")
async def prometheus_http_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    endpoint = request.url.path
    method = request.method
    status = str(response.status_code)

    # Track request count
    HTTP_REQUESTS_TOTAL.labels(method=method, endpoint=endpoint, status=status).inc()

    # Track latency
    HTTP_REQUEST_DURATION.labels(endpoint=endpoint).observe(duration)

    return response
