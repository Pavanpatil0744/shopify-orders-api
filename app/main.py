from fastapi import FastAPI, Response, HTTPException
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from .shopify import fetch_orders, fetch_order_by_id
from .metrics import SHOPIFY_ORDER_FETCH_COUNT

app = FastAPI()

@app.get("/orders")
async def get_shopify_orders():
    return await fetch_orders()

@app.get("/orders/{order_id}")
async def get_shopify_order(order_id: int):
    order = await fetch_order_by_id(order_id)
    if order:
        SHOPIFY_ORDER_FETCH_COUNT.labels(status="success").inc()
        return order
    else:
        SHOPIFY_ORDER_FETCH_COUNT.labels(status="not_found").inc()
        raise HTTPException(status_code=404, detail="Order not found")
    
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
