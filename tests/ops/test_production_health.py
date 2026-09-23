import pytest
from app.services.ephemeris_sync_service import ephemeris_sync_service
from app.middleware.observability_middleware import observability_middleware

def test_production_health_liveness_and_readiness_checks():
    sync_res = ephemeris_sync_service.sync_ephemeris_files()
    assert sync_res["status"] == "SYNCED"
    assert sync_res["ephemeris_path_valid"] is True

def test_production_health_prometheus_metrics_export():
    observability_middleware.record_request_metrics(duration_sec=0.035, confluence_score=85.0)
    metrics_text = observability_middleware.generate_prometheus_metrics_text()

    assert "api_request_throughput_total" in metrics_text
    assert "astrology_calculation_latency_seconds" in metrics_text
    assert "prediction_confluence_score_distribution" in metrics_text
