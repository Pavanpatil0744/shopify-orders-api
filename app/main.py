from fastapi import FastAPI, Response, HTTPException, Request
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from .shopify import fetch_orders, fetch_order_by_id, update_order

app = FastAPI()


@app.get("/orders")
async def get_all_orders():
    return await fetch_orders()


@app.get("/orders/{order_id}")
async def get_order(order_id: int):
    return await fetch_order_by_id(order_id)


@app.put("/orders/{order_id}")
async def modify_order(order_id: int, request: Request):
    payload = await request.json()
    return await update_order(order_id, payload)


@app.get("/metrics")
def get_metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/health")
def health_check():
    return {"status": "ok"}
