import httpx
import time
from .config import SHOPIFY_STORE_DOMAIN, SHOPIFY_ACCESS_TOKEN
from .metrics import (
    SHOPIFY_ORDER_FETCH_COUNT,
    SHOPIFY_ORDER_FETCH_DURATION,
    SHOPIFY_ORDER_TOTAL_RETURNED,
    SHOPIFY_ORDER_REVENUE_INR,
    SHOPIFY_ORDER_LAST_SUCCESS_TS,
)

API_VERSION = "2024-04"
BASE_URL = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/{API_VERSION}"

headers = {
    "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
    "Content-Type": "application/json"
}

async def fetch_orders():
    url = f"{BASE_URL}/orders.json"
    start_time = time.time()

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            duration = time.time() - start_time
            SHOPIFY_ORDER_FETCH_DURATION.observe(duration)

            if response.status_code == 200:
                SHOPIFY_ORDER_FETCH_COUNT.labels(status="success").inc()

                data = response.json()
                orders = data.get("orders", [])

                # Metrics update
                SHOPIFY_ORDER_TOTAL_RETURNED.set(len(orders))
                SHOPIFY_ORDER_LAST_SUCCESS_TS.set(time.time())

                total_revenue = sum(float(order.get("total_price", 0)) for order in orders)
                SHOPIFY_ORDER_REVENUE_INR.inc(total_revenue)

                return data
            else:
                SHOPIFY_ORDER_FETCH_COUNT.labels(status="error").inc()
                return {"error": f"Failed with status {response.status_code}"}
        except Exception as e:
            SHOPIFY_ORDER_FETCH_COUNT.labels(status="exception").inc()
            return {"error": str(e)}

async def fetch_order_by_id(order_id: int):
    url = f"{BASE_URL}/orders/{order_id}.json"
    start_time = time.time()

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            duration = time.time() - start_time
            SHOPIFY_ORDER_FETCH_DURATION.observe(duration)

            if response.status_code == 200:
                SHOPIFY_ORDER_FETCH_COUNT.labels(status="success").inc()
                return response.json()
            elif response.status_code == 404:
                SHOPIFY_ORDER_FETCH_COUNT.labels(status="not_found").inc()
                return None
            else:
                SHOPIFY_ORDER_FETCH_COUNT.labels(status="error").inc()
                return {"error": f"Failed with status {response.status_code}"}
        except Exception as e:
            SHOPIFY_ORDER_FETCH_COUNT.labels(status="exception").inc()
            return {"error": str(e)}
