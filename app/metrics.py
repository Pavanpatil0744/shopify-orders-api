from prometheus_client import Counter

SHOPIFY_ORDER_FETCH_COUNT = Counter(
    "shopify_orders_fetch_total",
    "Count of order fetch attempts",
    ["status"]  # success, error, exception, not_found
)
