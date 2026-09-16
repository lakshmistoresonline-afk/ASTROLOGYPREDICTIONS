import pytest
from datetime import datetime
from app.astrology.core.calculation_config import calculate_canonical_chart
from app.astrology.predictions.temporal_rules import TEMPORAL_EVENT_RULES, TEMPORAL_RULE_REGISTRY_VERSION
from app.astrology.predictions.temporal_activation import evaluate_temporal_activation, TemporalActivationResult, ASPECT_RULES
from app.astrology.predictions.evidence import EvidenceGraph, calculate_score_from_evidence
from app.astrology.predictions.engine import generate_evidence_based_predictions, PREDICTION_ENGINE_VERSION

def test_p03_r39_engine_version():
    assert PREDICTION_ENGINE_VERSION == "P0.3-R41"
    assert TEMPORAL_RULE_REGISTRY_VERSION == "P0.3-R41"

def test_p03_r39_aspect_rules_completeness():
    assert len(ASPECT_RULES) >= 5
    for asp, spec in ASPECT_RULES.items():
        assert "angle" in spec
        assert "max_orb" in spec
        assert "magnitude" in spec
        assert "polarity" in spec

def test_p03_r39_multiple_event_requests_temporal():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    target_dt = datetime(2026, 1, 1, 12, 0)

    res = generate_evidence_based_predictions(
        chart,
        selected_date=target_dt,
        event_requests={"Career": "PROMOTION", "Finance": "INCOME_EXPANSION"}
    )
    assert res is not None
    assert "temporal_activation_by_event" in res
    assert "PROMOTION" in res["temporal_activation_by_event"]
    assert "INCOME_EXPANSION" in res["temporal_activation_by_event"]

def test_p03_r39_true_target_date_variance_master():
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

def test_p03_r39_transit_failure_mutation(monkeypatch):
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    target_dt = datetime(2026, 1, 1, 12, 0)

    def mock_calc_fail(jd, pid):
        raise RuntimeError("Simulated Ephemeris Failure")

    monkeypatch.setattr("app.astrology.core.ephemeris.get_planet_position", mock_calc_fail)

    with pytest.raises(RuntimeError, match="CALCULATION_ENGINE_UNAVAILABLE"):
        evaluate_temporal_activation(chart, target_dt, domain="CAREER", event_type="PROMOTION")
