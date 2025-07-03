from prometheus_client import Counter, Histogram

# Count of fetch requests
SHOPIFY_ORDER_FETCH_COUNT = Counter(
    "shopify_orders_fetch_total",
    "Count of order fetch attempts",
    ["status", "type"]  # type: all / single; status: 200, 404, 500
)

# Duration of fetch requests
SHOPIFY_ORDER_FETCH_DURATION = Histogram(
    "shopify_order_fetch_duration_seconds",
    "Time spent processing Shopify order requests"
)

# Total revenue collected in INR
SHOPIFY_ORDER_REVENUE_INR = Counter(
    "shopify_order_revenue_inr_total",
    "Total revenue from all fetched orders in INR"
)

# Orders fetched per customer
SHOPIFY_ORDERS_PER_CUSTOMER = Counter(
    "shopify_orders_per_customer_total",
    "Number of orders per customer",
    ["email"]
)

# Product sales count
SHOPIFY_ITEM_SALES = Counter(
    "shopify_item_sales_total",
    "Number of items sold by product title",
    ["product_title"]
)
