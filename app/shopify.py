import httpx
from .config import SHOPIFY_STORE_DOMAIN, SHOPIFY_ACCESS_TOKEN
from .metrics import SHOPIFY_ORDER_FETCH_COUNT

async def fetch_orders():
    url = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/2024-04/orders.json"
    headers = {
        "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
        "Content-Type": "application/json"
    }

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
