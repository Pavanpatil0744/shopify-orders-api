import time
import httpx
import threading
from fastapi import HTTPException
from starlette.responses import JSONResponse
from prometheus_client import start_http_server

from config import SHOPIFY_STORE_DOMAIN, SHOPIFY_ACCESS_TOKEN
from metrics import (
    SHOPIFY_ORDER_FETCH_COUNT,
    SHOPIFY_ORDER_FETCH_DURATION,
    SHOPIFY_ORDER_REVENUE_INR,
    SHOPIFY_ORDERS_PER_CUSTOMER,
    SHOPIFY_ITEM_SALES,
)

# Start Prometheus metrics server on port 8000
threading.Thread(target=start_http_server, args=(8000,), daemon=True).start()


def update_metrics(order):
    """Update Prometheus metrics based on order data."""
    try:
        total = float(order.get("total_price", 0))
        SHOPIFY_ORDER_REVENUE_INR.inc(total)
        SHOPIFY_ORDERS_PER_CUSTOMER.labels(order.get("contact_email", "unknown")).inc()
        for item in order.get("line_items", []):
            SHOPIFY_ITEM_SALES.labels(product_title=item.get("title", "unknown")).inc(item.get("quantity", 0))
    except Exception as e:
        print(f"Metric update failed: {e}")


async def fetch_orders():
    start = time.time()
    url = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/2023-01/orders.json"
    headers = {
        "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
        "Content-Type": "application/json"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            for order in data.get("orders", []):
                update_metrics(order)

            SHOPIFY_ORDER_FETCH_COUNT.labels(status="200", type="all").inc()
            return data

        else:
            SHOPIFY_ORDER_FETCH_COUNT.labels(status="500", type="all").inc()
            raise HTTPException(status_code=response.status_code, detail=response.text)

    finally:
        SHOPIFY_ORDER_FETCH_DURATION.observe(time.time() - start)


async def fetch_order_by_id(order_id: int):
    start = time.time()
    url = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/2023-01/orders/{order_id}.json"
    headers = {
        "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
        "Content-Type": "application/json"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)

        if response.status_code == 200:
            order = response.json().get("order")
            update_metrics(order)
            SHOPIFY_ORDER_FETCH_COUNT.labels(status="200", type="single").inc()
            return order

        elif response.status_code == 404:
            SHOPIFY_ORDER_FETCH_COUNT.labels(status="404", type="single").inc()
            raise HTTPException(status_code=404, detail="Order not found")

        else:
            SHOPIFY_ORDER_FETCH_COUNT.labels(status="500", type="single").inc()
            raise HTTPException(status_code=response.status_code, detail=response.text)

    finally:
        SHOPIFY_ORDER_FETCH_DURATION.observe(time.time() - start)


async def update_order(order_id: int, payload: dict):
    start = time.time()
    url = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/2023-01/orders/{order_id}.json"
    headers = {
        "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
        "Content-Type": "application/json"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.put(url, json=payload, headers=headers)

        if response.status_code in (200, 201):
            SHOPIFY_ORDER_FETCH_COUNT.labels(status="200", type="update").inc()
            return response.json()

        else:
            SHOPIFY_ORDER_FETCH_COUNT.labels(status="500", type="update").inc()
            raise HTTPException(status_code=response.status_code, detail=response.text)

    finally:
        SHOPIFY_ORDER_FETCH_DURATION.observe(time.time() - start)
