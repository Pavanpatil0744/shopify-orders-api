from prometheus_client import Counter, Histogram, Gauge

SHOPIFY_ORDER_FETCH_COUNT = Counter(
    "shopify_orders_fetch_total",
    "Count of order fetch attempts",
    ["status"]  # success, error, not_found, exception
)

SHOPIFY_ORDER_FETCH_DURATION = Histogram(
    "shopify_orders_fetch_duration_seconds",
    "Time taken to fetch orders from Shopify",
    buckets=[0.1, 0.3, 0.5, 1, 2, 5]
)

SHOPIFY_ORDER_TOTAL_RETURNED = Gauge(
    "shopify_orders_returned_total",
    "Number of orders returned in last successful fetch"
)

SHOPIFY_ORDER_REVENUE_INR = Counter(
    "shopify_orders_revenue_inr_total",
    "Total order revenue calculated (approx) in INR"
)

SHOPIFY_ORDER_LAST_SUCCESS_TS = Gauge(
    "shopify_orders_last_success_timestamp",
    "Epoch time when last order fetch was successful"
)
