from fastapi import HTTPException
from prometheus_client import start_http_server
from starlette.responses import JSONResponse
import time
import json
import threading

from metrics import (
    SHOPIFY_ORDER_FETCH_COUNT,
    SHOPIFY_ORDER_FETCH_DURATION,
    SHOPIFY_ORDER_REVENUE_INR,
    SHOPIFY_ORDERS_PER_CUSTOMER,
    SHOPIFY_ITEM_SALES,
)

# Load orders from JSON once
with open("orders.json") as f:
    ORDERS = json.load(f)["orders"]

# Start Prometheus metrics HTTP server (on /metrics)
threading.Thread(target=start_http_server, args=(8000,), daemon=True).start()


def update_metrics(order):
    """Update custom metrics for a single order."""
    total = float(order.get("total_price", 0))
    SHOPIFY_ORDER_REVENUE_INR.inc(total)
    SHOPIFY_ORDERS_PER_CUSTOMER.labels(order.get("contact_email", "unknown")).inc()

    for item in order.get("line_items", []):
        SHOPIFY_ITEM_SALES.labels(product_title=item.get("title", "unknown")).inc(item.get("quantity", 0))


async def fetch_orders():
    start = time.time()
    try:
        for order in ORDERS:
            update_metrics(order)

        SHOPIFY_ORDER_FETCH_COUNT.labels(status="200", type="all").inc()
        return {"orders": ORDERS}

    except Exception as e:
        SHOPIFY_ORDER_FETCH_COUNT.labels(status="500", type="all").inc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        SHOPIFY_ORDER_FETCH_DURATION.observe(time.time() - start)


async def fetch_order_by_id(order_id: int):
    start = time.time()
    try:
        order = next((o for o in ORDERS if o["id"] == order_id), None)

        if order:
            update_metrics(order)
            SHOPIFY_ORDER_FETCH_COUNT.labels(status="200", type="single").inc()
            return order
        else:
            SHOPIFY_ORDER_FETCH_COUNT.labels(status="404", type="single").inc()
            raise HTTPException(status_code=404, detail="Order not found")

    except Exception as e:
        SHOPIFY_ORDER_FETCH_COUNT.labels(status="500", type="single").inc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        SHOPIFY_ORDER_FETCH_DURATION.observe(time.time() - start)


def health_check():
    return JSONResponse(content={"status": "ok"})
