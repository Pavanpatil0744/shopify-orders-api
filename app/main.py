from fastapi import FastAPI, Response, HTTPException
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from shopify import fetch_orders, fetch_order_by_id

app = FastAPI()

@app.get("/orders")
async def get_orders():
    return {"orders": await fetch_orders()}

@app.get("/orders/{order_id}")
async def get_order(order_id: int):
    return await fetch_order_by_id(order_id)

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/health")
def health():
    return {"status": "ok"}
