from prometheus_client import Counter, Histogram, Gauge

# --- Existing business metrics ---
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

# --- New HTTP metrics (for availability/latency SLI) ---
HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Total HTTP requests received",
    ["method", "endpoint", "status"]
)

HTTP_REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "Duration of HTTP requests in seconds",
    ["method", "endpoint", "status"],
    buckets=[0.1, 0.3, 0.5, 1, 2, 5]
)


# --- Business SLO metrics ---
TOTAL_VALID_REQUEST = Counter(
    "business_valid_requests_total",
    "Total valid business requests"
)

TOTAL_SUCCESSFUL_REQUEST = Counter(
    "business_successful_requests_total",
    "Total successful business requests"
)

SUCCESSFUL_RESPONSE_PERCENT = Gauge(
    "business_successful_response_percent",
    "Percentage of successful responses"
)

SLO_TARGET_PERCENT = Gauge(
    "business_slo_target_percent",
    "Configured SLO target percentage"
)

ERROR_BUDGET_ALLOCATED = Gauge(
    "business_error_budget_allocated",
    "Total error budget allocated (count)"
)

ERROR_BUDGET_USED = Gauge(
    "business_error_budget_used",
    "Error budget consumed (count)"
)

ERROR_BUDGET_LEFT = Gauge(
    "business_error_budget_left",
    "Error budget remaining (count)"
)
