import httpx
from .config import SHOPIFY_STORE_DOMAIN, SHOPIFY_ACCESS_TOKEN
from .metrics import SHOPIFY_ORDER_FETCH_COUNT

API_VERSION = "2024-04"
BASE_URL = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/{API_VERSION}"

headers = {
    "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
    "Content-Type": "application/json"
}

async def fetch_orders():
    url = f"{BASE_URL}/orders.json"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            if response.status_code == 200:
                SHOPIFY_ORDER_FETCH_COUNT.labels(status="success").inc()
                return response.json()
            else:
                SHOPIFY_ORDER_FETCH_COUNT.labels(status="error").inc()
                return {"error": f"Failed with status {response.status_code}"}
        except Exception as e:
            SHOPIFY_ORDER_FETCH_COUNT.labels(status="exception").inc()
            return {"error": str(e)}

async def fetch_order_by_id(order_id: int):
    url = f"{BASE_URL}/orders/{order_id}.json"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return None
            else:
                return {"error": f"Failed with status {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}
