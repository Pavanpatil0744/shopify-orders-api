import time
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from .metrics import HTTP_REQUESTS_TOTAL, HTTP_REQUEST_DURATION

# Create FastAPI app
app = FastAPI()


# Middleware for Prometheus
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

        # Track latency
        HTTP_REQUEST_DURATION.labels(
            method=method,
            endpoint=endpoint,
            status=status
        ).observe(duration)

        return response


# Add middleware
app.add_middleware(PrometheusMiddleware)


# --- ROUTES ---
@app.get("/")
def root():
    return {"message": "App is running!"}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
