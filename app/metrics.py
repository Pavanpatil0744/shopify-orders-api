from prometheus_client import Counter, Histogram

SHOPIFY_ORDER_FETCH_COUNT = Counter(
    "shopify_orders_fetch_total",
    "Total Shopify orders fetched",
    ["status", "type"]
)

SHOPIFY_ORDER_FETCH_DURATION = Histogram(
    "shopify_order_fetch_duration_seconds",
    "Duration of Shopify order fetch in seconds"
)

SHOPIFY_ORDER_REVENUE_INR = Counter(
    "shopify_order_revenue_inr_total",
    "Total revenue of orders in INR"
)

SHOPIFY_ORDERS_PER_CUSTOMER = Counter(
    "shopify_orders_per_customer_total",
    "Orders per customer",
    ["email"]
)

SHOPIFY_ITEM_SALES = Counter(
    "shopify_item_sales_total",
    "Total items sold by product title",
    ["product_title"]
)
