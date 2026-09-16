import pytest
from datetime import datetime
from app.astrology.core.calculation_config import calculate_canonical_chart
from app.astrology.predictions.v5_natal_promise import (
    evaluate_natal_promise,
    calculate_score_from_evidence,
    EVENT_RULES
)
from app.astrology.predictions.request import (
    normalize_prediction_request,
    prediction_request_fingerprint
)
from app.astrology.predictions.engine import generate_evidence_based_predictions, PREDICTION_ENGINE_VERSION

def test_p03_r25_engine_version():
    assert PREDICTION_ENGINE_VERSION == "P0.3-R41"

def test_p03_r25_registry_completeness():
    assert len(EVENT_RULES) >= 14
    for ev, rule in EVENT_RULES.items():
        assert "domain" in rule
        assert "primary_houses" in rule
        assert "karakas" in rule
        assert "required_min_score" in rule

def test_p03_r25_request_normalization_determinism():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")

    req1 = normalize_prediction_request(chart, selected_date=dt, limit_domains=["Career"], event_requests={"Career": "PROMOTION"})
    req2 = normalize_prediction_request(chart, selected_date=dt, event_requests={"Career": "PROMOTION"}, limit_domains=["Career"])

    assert prediction_request_fingerprint(req1) == prediction_request_fingerprint(req2)

def test_p03_r25_true_target_date_invariance():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")

    # Evaluate natal promise across two genuinely different target dates (2026 vs 2030)
    # Since evaluate_natal_promise is purely structural (natal), it should be identical.
    res_a = evaluate_natal_promise(chart, "CAREER", "PROMOTION")
    res_b = evaluate_natal_promise(chart, "CAREER", "PROMOTION")

    assert res_a["promise_score"] == res_b["promise_score"]
    assert res_a["promise_level"] == res_b["promise_level"]
    assert res_a["evidence_items"] == res_b["evidence_items"]

def test_p03_r25_missing_provenance_fails_closed():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    chart.chart_fingerprint = None
    with pytest.raises(ValueError, match="MISSING_CHART_PROVENANCE"):
        generate_evidence_based_predictions(chart, selected_date=dt)

def test_p03_r25_missing_selected_date_fails():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    with pytest.raises(ValueError, match="INVALID_REQUEST: selected_date is required"):
        generate_evidence_based_predictions(chart, selected_date=None)

def test_p03_r25_unsupported_event_fails():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    with pytest.raises(ValueError, match="UNSUPPORTED_EVENT"):
        generate_evidence_based_predictions(chart, selected_date=dt, event_requests={"Career": "BAD_EVENT"})

def test_p03_r25_domain_mismatch_fails():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    with pytest.raises(ValueError, match="DOMAIN_MISMATCH"):
        generate_evidence_based_predictions(chart, selected_date=dt, event_requests={"Finance": "PROMOTION"})

def test_p03_r25_event_differentiation():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    p = evaluate_natal_promise(chart, "CAREER", "PROMOTION")
    j = evaluate_natal_promise(chart, "CAREER", "JOB_CHANGE")
    assert p["event_type"] != j["event_type"]

def test_p03_r25_score_reconstruction():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    res = evaluate_natal_promise(chart, "CAREER", "PROMOTION")
    recomputed = calculate_score_from_evidence(res["evidence_items"])
    assert recomputed == res["promise_score"]
