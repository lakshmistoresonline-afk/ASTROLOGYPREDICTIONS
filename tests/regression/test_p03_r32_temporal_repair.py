import pytest
from datetime import datetime
from app.astrology.core.calculation_config import calculate_canonical_chart
from app.astrology.predictions.v5_natal_promise import evaluate_natal_promise, EVENT_RULES
from app.astrology.predictions.request import normalize_prediction_request, prediction_request_fingerprint
from app.astrology.predictions.temporal_activation import evaluate_temporal_activation, TemporalActivationResult
from app.astrology.predictions.engine import generate_evidence_based_predictions, PREDICTION_ENGINE_VERSION

def test_p03_r32_engine_version():
    assert PREDICTION_ENGINE_VERSION == "P0.3-R40"

def test_p03_r32_true_target_date_invariance_master():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")

    target_a = datetime(2026, 1, 1, 10, 0)
    target_b = datetime(2030, 1, 1, 10, 0)

    res_a = generate_evidence_based_predictions(chart, selected_date=target_a, limit_domains=["Career"], event_requests={"Career": "PROMOTION"})
    res_b = generate_evidence_based_predictions(chart, selected_date=target_b, limit_domains=["Career"], event_requests={"Career": "PROMOTION"})

    assert res_a is not None
    assert res_b is not None
    assert "temporal_activation" in res_a
    assert "temporal_activation" in res_b
    assert res_a["temporal_activation"]["target_datetime"] != res_b["temporal_activation"]["target_datetime"]

def test_p03_r32_transit_failure_mutation(monkeypatch):
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    target_dt = datetime(2026, 1, 1, 12, 0)

    def mock_calc_fail(jd):
        raise RuntimeError("Simulated Ephemeris Failure")

    monkeypatch.setattr("app.astrology.core.ephemeris.get_planet_position", mock_calc_fail)

    with pytest.raises(RuntimeError, match="CALCULATION_ENGINE_UNAVAILABLE"):
        evaluate_temporal_activation(chart, target_dt, domain="CAREER", event_type="PROMOTION")

def test_p03_r32_missing_selected_date_fails():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    with pytest.raises(ValueError, match="INVALID_REQUEST: selected_date is required"):
        generate_evidence_based_predictions(chart, selected_date=None)

def test_p03_r32_unsupported_event_fails():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    with pytest.raises(ValueError, match="UNSUPPORTED_EVENT"):
        generate_evidence_based_predictions(chart, selected_date=dt, event_requests={"Career": "BAD_EVENT"})

def test_p03_r32_domain_mismatch_fails():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    with pytest.raises(ValueError, match="DOMAIN_MISMATCH"):
        generate_evidence_based_predictions(chart, selected_date=dt, event_requests={"Finance": "PROMOTION"})
