from fastapi import FastAPI, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from .shopify import fetch_orders

app = FastAPI()

@app.get("/orders")
async def get_shopify_orders():
    return await fetch_orders()

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
