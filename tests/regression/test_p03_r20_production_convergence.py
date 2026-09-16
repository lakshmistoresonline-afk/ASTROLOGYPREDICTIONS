import pytest
from datetime import datetime
from app.astrology.core.calculation_config import calculate_canonical_chart
from app.astrology.predictions.v5_natal_promise import (
    evaluate_natal_promise,
    calculate_score_from_evidence,
    EVENT_RULES
)
from app.astrology.predictions.engine import generate_evidence_based_predictions, PREDICTION_ENGINE_VERSION

def test_p03_r20_engine_version():
    assert PREDICTION_ENGINE_VERSION == "P0.3-R40"

def test_p03_r20_missing_selected_date_fails():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    with pytest.raises(ValueError, match="INVALID_REQUEST: selected_date is required"):
        generate_evidence_based_predictions(chart, selected_date=None)

def test_p03_r20_unsupported_event_fails():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    with pytest.raises(ValueError, match="UNSUPPORTED_EVENT"):
        generate_evidence_based_predictions(chart, selected_date=dt, event_requests={"Career": "BAD_EVENT"})

def test_p03_r20_domain_mismatch_fails():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    with pytest.raises(ValueError, match="DOMAIN_MISMATCH"):
        generate_evidence_based_predictions(chart, selected_date=dt, event_requests={"Finance": "PROMOTION"})

def test_p03_r20_natal_date_invariance():
    dt1 = datetime(1990, 9, 10, 14, 30)
    chart1 = calculate_canonical_chart(dt1, 10.5276, 76.2144, "Asia/Kolkata")
    res1 = evaluate_natal_promise(chart1, "CAREER", "PROMOTION")
    res2 = evaluate_natal_promise(chart1, "CAREER", "PROMOTION")
    assert res1["promise_score"] == res2["promise_score"]
    assert res1["promise_level"] == res2["promise_level"]
    assert res1["evidence_items"] == res2["evidence_items"]

def test_p03_r20_cache_fail_closed():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    chart.calculation_config_fingerprint = None
    with pytest.raises(ValueError, match="CACHE_FAIL_CLOSED"):
        generate_evidence_based_predictions(chart, selected_date=dt)
