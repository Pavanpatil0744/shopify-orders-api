import time
from fastapi import FastAPI, Request, Response, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from .metrics import HTTP_REQUESTS_TOTAL, HTTP_REQUEST_DURATION
from .shopify import fetch_orders, fetch_order_by_id


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
@app.get("/orders")
async def get_shopify_orders():
    return await fetch_orders()


@app.get("/orders/{order_id}")
async def get_shopify_order(order_id: int):
    order = await fetch_order_by_id(order_id)
    if order:
        return order
    else:
        raise HTTPException(status_code=404, detail="Order not found")


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
