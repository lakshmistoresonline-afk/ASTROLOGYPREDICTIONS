"""
Telemetry & Metrics Configuration (Module 30 - Part 3).
Configures OpenTelemetry P99 latency tracking, token usage / cost metrics, and Redis cache hit ratios.
"""
from typing import Dict, Any

TELEMETRY_CONFIG = {
    "service_name": "astrology-predictions-api",
    "prometheus_endpoint": "/metrics",
    "tracing": {
        "enabled": True,
        "sampler_ratio": 1.0, # 100% trace sampling for high reliability
        "spans": ["Pass_1_Data_Prep", "Pass_2_Core_Narrative", "Pass_3_Remedies_Synthesis"]
    },
    "alert_thresholds": {
        "max_p99_latency_ms": 15000, # Alert if P99 latency > 15 seconds
        "max_cost_per_report_usd": 0.05,
        "min_redis_cache_hit_ratio": 0.85
    }
}
