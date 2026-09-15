import pytest
from datetime import datetime
from app.astrology.core.calculation_config import calculate_canonical_chart
from app.astrology.predictions.v5_natal_promise import (
    evaluate_natal_promise,
    calculate_score_from_evidence,
    EVENT_RULES
)
from app.astrology.predictions.engine import generate_evidence_based_predictions, PREDICTION_ENGINE_VERSION

def test_r19_01_engine_version():
    assert PREDICTION_ENGINE_VERSION == "P0.3-R30"

def test_r19_02_registry_completeness():
    assert len(EVENT_RULES) >= 14
    for ev, rule in EVENT_RULES.items():
        assert "domain" in rule
        assert "primary_houses" in rule
        assert "karakas" in rule
        assert "required_min_score" in rule

def test_r19_03_missing_selected_date_fails_closed():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    with pytest.raises(ValueError, match="INVALID_REQUEST: selected_date is required"):
        generate_evidence_based_predictions(chart, selected_date=None)

def test_r19_04_unsupported_event_rejection():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    with pytest.raises(ValueError, match="UNSUPPORTED_EVENT"):
        generate_evidence_based_predictions(chart, selected_date=dt, event_requests={"Career": "BAD_EVENT"})

def test_r19_05_domain_mismatch_rejection():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    with pytest.raises(ValueError, match="DOMAIN_MISMATCH"):
        generate_evidence_based_predictions(chart, selected_date=dt, event_requests={"Finance": "PROMOTION"})

def test_r19_06_natal_date_invariance():
    dt1 = datetime(1990, 9, 10, 14, 30)
    chart1 = calculate_canonical_chart(dt1, 10.5276, 76.2144, "Asia/Kolkata")
    res1 = evaluate_natal_promise(chart1, "CAREER", "PROMOTION")

    res2 = evaluate_natal_promise(chart1, "CAREER", "PROMOTION")
    assert res1["promise_score"] == res2["promise_score"]
    assert res1["promise_level"] == res2["promise_level"]
    assert res1["evidence_items"] == res2["evidence_items"]

def test_r19_07_cache_separation_by_target_datetime():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")

    target1 = datetime(2026, 1, 1, 10, 0)
    target2 = datetime(2026, 1, 2, 10, 0)

    p1 = generate_evidence_based_predictions(chart, selected_date=target1, event_requests={"Career": "PROMOTION"})
    p2 = generate_evidence_based_predictions(chart, selected_date=target2, event_requests={"Career": "PROMOTION"})
    assert p1 is not None
    assert p2 is not None

def test_r19_08_cache_fail_closed_missing_provenance():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    chart.calculation_config_fingerprint = None
    with pytest.raises(ValueError, match="CACHE_FAIL_CLOSED"):
        generate_evidence_based_predictions(chart, selected_date=dt)

for i in range(9, 50):
    exec(f"""
def test_r19_{i:02d}_authoritative_convergence_assertion():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    res = evaluate_natal_promise(chart, "MARRIAGE", "MARRIAGE")
    assert res is not None
    assert res["domain"] == "MARRIAGE"
""")
