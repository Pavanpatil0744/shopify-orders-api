# ✅ metrics.py
from prometheus_client import Counter, Histogram

SHOPIFY_ORDER_FETCH_COUNT = Counter(
    "shopify_orders_fetch_total",
    "Count of order fetch attempts",
    ["status", "type"]
)

SHOPIFY_ORDER_FETCH_DURATION = Histogram(
    "shopify_orders_fetch_duration_seconds",
    "Time taken to fetch Shopify orders"
)

SHOPIFY_ORDER_REVENUE_INR = Counter(
    "shopify_orders_total_revenue_inr",
    "Total Shopify order revenue in INR"
)

SHOPIFY_ORDERS_PER_CUSTOMER = Counter(
    "shopify_orders_per_customer_total",
    "Number of orders per customer",
    ["customer_email"]
)

SHOPIFY_ITEM_SALES = Counter(
    "shopify_product_sales_total",
    "Total sales per product title",
    ["product_title"]
)
