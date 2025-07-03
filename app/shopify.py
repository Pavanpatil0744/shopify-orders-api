import httpx
import time
from fastapi import HTTPException
from config import SHOPIFY_STORE_DOMAIN, SHOPIFY_ACCESS_TOKEN
from metrics import (
    SHOPIFY_ORDER_FETCH_COUNT,
    SHOPIFY_ORDER_FETCH_DURATION,
    SHOPIFY_ORDER_REVENUE_INR,
    SHOPIFY_ORDERS_PER_CUSTOMER,
    SHOPIFY_ITEM_SALES,
)

def update_metrics(order):
    try:
        SHOPIFY_ORDER_REVENUE_INR.inc(float(order.get("total_price", 0)))
        SHOPIFY_ORDERS_PER_CUSTOMER.labels(order.get("contact_email", "unknown")).inc()
        for item in order.get("line_items", []):
            SHOPIFY_ITEM_SALES.labels(product_title=item.get("title", "unknown")).inc(item.get("quantity", 0))
    except Exception as e:
        print(f"[metrics error]: {e}")

async def fetch_orders():
    start = time.time()
    url = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/2023-01/orders.json"
    headers = {"X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    duration = time.time() - start
    SHOPIFY_ORDER_FETCH_DURATION.observe(duration)

    if response.status_code == 200:
        data = response.json()
        orders = data.get("orders", [])
        for order in orders:
            update_metrics(order)
        SHOPIFY_ORDER_FETCH_COUNT.labels(status="200", type="all").inc()
        return orders
    else:
        SHOPIFY_ORDER_FETCH_COUNT.labels(status="500", type="all").inc()
        raise HTTPException(status_code=response.status_code, detail=response.text)

async def fetch_order_by_id(order_id: int):
    start = time.time()
    url = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/2023-01/orders/{order_id}.json"
    headers = {"X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    duration = time.time() - start
    SHOPIFY_ORDER_FETCH_DURATION.observe(duration)

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
