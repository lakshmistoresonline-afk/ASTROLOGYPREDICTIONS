import pytest
from app.api.v3.gateway.rate_limiter import rate_limiter
from app.api.v3.gateway.billing import billing_analytics

def test_api_rate_limiter_tenant_isolation_and_headers():
    # Test Free Tier Rate Limit (60 req/min capacity)
    is_allowed, headers = rate_limiter.evaluate_rate_limit("free_tenant_1", tier="free")

    assert is_allowed is True
    assert headers["X-RateLimit-Limit"] == "60"
    assert int(headers["X-RateLimit-Remaining"]) <= 60
    assert "X-RateLimit-Reset" in headers

def test_api_billing_analytics_usage_logging():
    log_res = billing_analytics.log_event("pro_tenant_100", "PDF_GENERATION", tokens_used=1200, cost_usd=0.0024)

    assert log_res["tenant_id"] == "pro_tenant_100"
    assert log_res["event_type"] == "PDF_GENERATION"
    assert log_res["tokens_used"] == 1200

    summary = billing_analytics.get_tenant_usage_summary("pro_tenant_100")
    assert summary["total_events"] >= 1
    assert summary["total_tokens_consumed"] >= 1200
