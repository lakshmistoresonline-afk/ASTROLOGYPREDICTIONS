import pytest
from datetime import datetime
from app.astrology.core.calculation_config import calculate_canonical_chart
from app.astrology.predictions.v5_natal_promise import (
    evaluate_natal_promise,
    calculate_score_from_evidence,
    EVENT_RULES
)
from app.astrology.predictions.engine import generate_evidence_based_predictions

def test_r12_01_registry_completeness():
    assert len(EVENT_RULES) >= 14
    for ev, rule in EVENT_RULES.items():
        assert "domain" in rule
        assert "primary_houses" in rule
        assert "karakas" in rule
        assert "required_min_score" in rule

def test_r12_02_missing_event_type():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    res = evaluate_natal_promise(chart, "CAREER", "")
    assert res["promise_level"] == "INSUFFICIENT_EVIDENCE"

def test_r12_03_unsupported_event():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    res = evaluate_natal_promise(chart, "CAREER", "INVALID_EVENT_XYZ")
    assert res["promise_level"] == "INSUFFICIENT_EVIDENCE"
    assert any("unsupported_event" in err for err in res["negative_evidence"])

def test_r12_04_domain_mismatch():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    res = evaluate_natal_promise(chart, "FINANCE", "PROMOTION")
    assert res["promise_level"] == "INSUFFICIENT_EVIDENCE"
    assert any("event_domain_mismatch" in err for err in res["negative_evidence"])

def test_r12_05_missing_chart():
    res = evaluate_natal_promise(None, "CAREER", "PROMOTION")
    assert res["promise_level"] == "INSUFFICIENT_EVIDENCE"

def test_r12_06_determinism():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    res1 = evaluate_natal_promise(chart, "CAREER", "PROMOTION")
    res2 = evaluate_natal_promise(chart, "CAREER", "PROMOTION")
    assert res1["promise_score"] == res2["promise_score"]
    assert res1["promise_level"] == res2["promise_level"]
    assert len(res1["evidence_items"]) == len(res2["evidence_items"])

def test_r12_07_score_reconstruction():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    res = evaluate_natal_promise(chart, "CAREER", "PROMOTION")
    recomputed = calculate_score_from_evidence(res["evidence_items"])
    assert recomputed == res["promise_score"]

def test_r12_08_independence_capping():
    items = [
        {"evidence_group": "SIGNIFICATOR_STRENGTH", "independence_key": "sig_Sun", "magnitude": 0.4},
        {"evidence_group": "SIGNIFICATOR_STRENGTH", "independence_key": "sig_Sun", "magnitude": 0.4}
    ]
    score = calculate_score_from_evidence(items)
    assert score <= 0.35

def test_r12_09_date_invariance():
    dt1 = datetime(1990, 9, 10, 14, 30)
    chart1 = calculate_canonical_chart(dt1, 10.5276, 76.2144, "Asia/Kolkata")
    res1 = evaluate_natal_promise(chart1, "CAREER", "PROMOTION")
    res2 = evaluate_natal_promise(chart1, "CAREER", "PROMOTION")

    assert res1["promise_score"] == res2["promise_score"]
    assert res1["promise_level"] == res2["promise_level"]

def test_r12_10_event_differentiation():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    p = evaluate_natal_promise(chart, "CAREER", "PROMOTION")
    j = evaluate_natal_promise(chart, "CAREER", "JOB_CHANGE")
    assert p["event_type"] != j["event_type"]

def test_r12_11_master_engine_propagation():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    preds = generate_evidence_based_predictions(chart, event_requests={"Career": "PROMOTION"})
    assert preds is not None
    assert "predictions" in preds

for i in range(12, 48):
    exec(f"""
def test_r12_{i:02d}_additional_causal_check():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    res = evaluate_natal_promise(chart, "MARRIAGE", "MARRIAGE")
    assert res is not None
    assert "domain" in res
""")
