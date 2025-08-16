from .metrics import (
    SHOPIFY_ORDER_FETCH_COUNT,
    SHOPIFY_ORDER_FETCH_DURATION,
    SHOPIFY_ORDER_TOTAL_RETURNED,
    SHOPIFY_ORDER_REVENUE_INR,
    SHOPIFY_ORDER_LAST_SUCCESS_TS,
    TOTAL_VALID_REQUEST,
    TOTAL_SUCCESSFUL_REQUEST,
    SUCCESSFUL_RESPONSE_PERCENT,
    SLO_TARGET_PERCENT,
    ERROR_BUDGET_ALLOCATED,
    ERROR_BUDGET_USED,
    ERROR_BUDGET_LEFT,
)

# configure your SLO target (example: 99.9% for 30 days)
SLO_TARGET = 99.9  

def update_business_sli(success: bool):
    """Helper to update business-level SLI & error budget usage"""
    TOTAL_VALID_REQUEST.inc()
    if success:
        TOTAL_SUCCESSFUL_REQUEST.inc()

    # Calculate success percentage
    valid = TOTAL_VALID_REQUEST._value.get()
    successful = TOTAL_SUCCESSFUL_REQUEST._value.get()
    if valid > 0:
        success_pct = (successful / valid) * 100
        SUCCESSFUL_RESPONSE_PERCENT.set(success_pct)
        SLO_TARGET_PERCENT.set(SLO_TARGET)

        # Error budget (per 30 days)
        # For 99.9%, allowed errors = 0.1% of total
        budget_allocated = valid * (100 - SLO_TARGET) / 100
        budget_used = valid - successful
        budget_left = max(budget_allocated - budget_used, 0)

        ERROR_BUDGET_ALLOCATED.set(budget_allocated)
        ERROR_BUDGET_USED.set(budget_used)
        ERROR_BUDGET_LEFT.set(budget_left)
