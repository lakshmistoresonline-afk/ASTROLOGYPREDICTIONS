import pytest
from datetime import datetime
from app.astrology.core.calculation_config import calculate_canonical_chart
from app.astrology.predictions.temporal_activation import evaluate_temporal_activation, TemporalActivationResult
from app.astrology.predictions.engine import generate_evidence_based_predictions, PREDICTION_ENGINE_VERSION

def test_p03_r31_engine_version():
    assert PREDICTION_ENGINE_VERSION == "P0.3-R32"

def test_p03_r31_temporal_activation_execution():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    target_dt = datetime(2026, 1, 1, 12, 0)

    act = evaluate_temporal_activation(chart, target_dt, domain="CAREER", event_type="PROMOTION")
    assert isinstance(act, TemporalActivationResult)
    assert act.target_datetime == target_dt
    assert "dasha_data" in act.to_dict()
    assert "transit_positions" in act.to_dict()

def test_p03_r31_true_target_date_invariance_master():
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

def test_p03_r31_missing_selected_date_fails():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    with pytest.raises(ValueError, match="INVALID_REQUEST: selected_date is required"):
        generate_evidence_based_predictions(chart, selected_date=None)

def test_p03_r31_unsupported_event_fails():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    with pytest.raises(ValueError, match="UNSUPPORTED_EVENT"):
        generate_evidence_based_predictions(chart, selected_date=dt, event_requests={"Career": "BAD_EVENT"})

def test_p03_r31_domain_mismatch_fails():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    with pytest.raises(ValueError, match="DOMAIN_MISMATCH"):
        generate_evidence_based_predictions(chart, selected_date=dt, event_requests={"Finance": "PROMOTION"})
