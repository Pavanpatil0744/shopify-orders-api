import httpx
import time
from app.config import SHOPIFY_API_BASE_URL, SHOPIFY_ACCESS_TOKEN
from app.metrics import (
    SHOPIFY_ORDER_FETCH_COUNT,
    SHOPIFY_ORDER_FETCH_DURATION,
    SHOPIFY_ORDER_REVENUE_INR,
    SHOPIFY_ORDERS_PER_CUSTOMER,
    SHOPIFY_ITEM_SALES,
)

headers = {
    "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
    "Content-Type": "application/json",
}

async def fetch_orders():
    start = time.time()
    try:
        url = f"{SHOPIFY_API_BASE_URL}/orders.json"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)

        SHOPIFY_ORDER_FETCH_COUNT.labels(status=str(response.status_code), type="all").inc()
        response.raise_for_status()
        data = response.json()

        for order in data.get("orders", []):
            SHOPIFY_ORDER_REVENUE_INR.inc(float(order.get("total_price", 0)))
            SHOPIFY_ORDERS_PER_CUSTOMER.labels(order.get("contact_email", "unknown")).inc()
            for item in order.get("line_items", []):
                SHOPIFY_ITEM_SALES.labels(product_title=item.get("title", "unknown")).inc(item.get("quantity", 0))

        return data

    finally:
        SHOPIFY_ORDER_FETCH_DURATION.observe(time.time() - start)

async def fetch_order_by_id(order_id: int):
    url = f"{SHOPIFY_API_BASE_URL}/orders/{order_id}.json"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response.json().get("order")

async def update_order_note(order_id: int, note: str):
    url = f"{SHOPIFY_API_BASE_URL}/orders/{order_id}.json"
    payload = {
        "order": {
            "id": order_id,
            "note": note
        }
    }
    async with httpx.AsyncClient() as client:
        response = await client.put(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json().get("order")
