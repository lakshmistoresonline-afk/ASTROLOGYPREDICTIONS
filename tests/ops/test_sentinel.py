import pytest
from app.ops.sentinel import ai_sentinel_controller

def test_ops_ai_sentinel_normal_operation():
    res = ai_sentinel_controller.evaluate_system_health_and_failover(redis_latency_ms=5.0, llm_latency_ms=1200.0)

    assert res["sentinel_status"] == "HEALTHY"
    assert res["redis_healthy"] is True
    assert res["llm_healthy"] is True
    assert len(res["active_failover_actions"]) == 0

def test_ops_ai_sentinel_redis_outage_failover():
    # Simulate high Redis latency (600ms > 500ms threshold)
    res = ai_sentinel_controller.evaluate_system_health_and_failover(redis_latency_ms=600.0)

    assert res["sentinel_status"] == "SELF_HEALING_ACTIVE"
    assert res["redis_healthy"] is False
    assert "REDIRECT_REDIS_L2_TO_L1_MEMORY_AND_CLIENT_WASM" in res["active_failover_actions"]

def test_ops_ai_sentinel_llm_timeout_failover():
    # Simulate LLM timeout (12000ms > 10000ms threshold)
    res = ai_sentinel_controller.evaluate_system_health_and_failover(llm_latency_ms=12000.0)

    assert res["sentinel_status"] == "SELF_HEALING_ACTIVE"
    assert res["llm_healthy"] is False
    assert "FALLBACK_LLM_TO_LOCAL_ON_DEVICE_SLM" in res["active_failover_actions"]
