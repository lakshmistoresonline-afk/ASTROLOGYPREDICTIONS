import pytest
from app.services.ephemeris_sync_service import ephemeris_sync_service
from app.middleware.observability_middleware import observability_middleware
from app.astrology.evaluation.historical_validation_harness import historical_validation_harness

def test_ops_ephemeris_sync_and_delta_t():
    sync_res = ephemeris_sync_service.sync_ephemeris_files()
    assert sync_res["status"] == "SYNCED"
    assert sync_res["current_delta_t_seconds"] > 0.0
    assert sync_res["ephemeris_path_valid"] is True

def test_ops_observability_metrics_and_anomaly_guardrail():
    observability_middleware.record_request_metrics(duration_sec=0.045, confluence_score=82.5)
    metrics_text = observability_middleware.generate_prometheus_metrics_text()

    assert "api_request_throughput_total" in metrics_text
    assert "astrology_calculation_latency_seconds" in metrics_text
    assert "prediction_confluence_score_distribution" in metrics_text

    # Test Anomaly Guardrail Interception
    is_anomaly = observability_middleware.check_payload_anomaly({})
    assert is_anomaly is True

def test_ops_historical_backtesting_accuracy_harness():
    report = historical_validation_harness.run_benchmark_evaluations()

    assert report["total_charts_tested"] >= 3
    assert report["accuracy_rate_percent"] >= 80.0
    assert report["benchmark_status"] == "PASSED"
    assert len(report["results"]) >= 3
