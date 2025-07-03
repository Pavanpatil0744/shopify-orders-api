from fastapi import FastAPI, Response, HTTPException
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from app.shopify import fetch_orders, fetch_order_by_id, update_order_note

app = FastAPI()

@app.get("/orders")
async def get_orders():
    return await fetch_orders()

@app.get("/orders/{order_id}")
async def get_order(order_id: int):
    order = await fetch_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.put("/orders/{order_id}/note")
async def put_order_note(order_id: int, note: str):
    try:
        updated = await update_order_note(order_id, note)
        return updated
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
