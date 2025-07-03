from prometheus_client import Counter, Histogram

SHOPIFY_ORDER_FETCH_COUNT = Counter(
    "shopify_orders_fetch_total", "Count of order fetch attempts", ["status", "type"]
)

SHOPIFY_ORDER_FETCH_DURATION = Histogram(
    "shopify_orders_fetch_duration_seconds", "Time taken to fetch orders from Shopify"
)

SHOPIFY_ORDER_REVENUE_INR = Counter(
    "shopify_order_total_revenue_inr", "Total revenue from orders (INR)"
)

SHOPIFY_ORDERS_PER_CUSTOMER = Counter(
    "shopify_orders_per_customer_total", "Total orders per customer", ["email"]
)

SHOPIFY_ITEM_SALES = Counter(
    "shopify_item_sales_total", "Total items sold by title", ["product_title"]
)
