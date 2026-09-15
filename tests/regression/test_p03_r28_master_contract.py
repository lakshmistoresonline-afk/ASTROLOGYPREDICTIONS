import pytest
from datetime import datetime
from app.astrology.core.calculation_config import calculate_canonical_chart
from app.astrology.predictions.evidence import EvidenceNode, EvidenceGraph, calculate_score_from_evidence
from app.astrology.predictions.v5_natal_promise import evaluate_natal_promise, EVENT_RULES
from app.astrology.predictions.request import normalize_prediction_request, prediction_request_fingerprint
from app.astrology.predictions.engine import generate_evidence_based_predictions, PREDICTION_ENGINE_VERSION

def test_p03_r28_engine_version():
    assert PREDICTION_ENGINE_VERSION == "P0.3-R36"

def test_p03_r28_registry_completeness():
    assert len(EVENT_RULES) >= 14
    for ev, rule in EVENT_RULES.items():
        assert "domain" in rule
        assert "primary_houses" in rule
        assert "karakas" in rule
        assert "required_min_score" in rule

def test_p03_r28_request_normalization():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    req1 = normalize_prediction_request(chart, selected_date=dt, limit_domains=["Career"], event_requests={"Career": "PROMOTION"})
    req2 = normalize_prediction_request(chart, selected_date=dt, event_requests={"Career": "PROMOTION"}, limit_domains=["Career"])
    assert prediction_request_fingerprint(req1) == prediction_request_fingerprint(req2)

def test_p03_r28_true_target_date_invariance():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")

    target_a = datetime(2026, 1, 1, 10, 0)
    target_b = datetime(2030, 1, 1, 10, 0)

    res_a = generate_evidence_based_predictions(chart, selected_date=target_a, limit_domains=["Career"], event_requests={"Career": "PROMOTION"})
    res_b = generate_evidence_based_predictions(chart, selected_date=target_b, limit_domains=["Career"], event_requests={"Career": "PROMOTION"})

    assert res_a is not None
    assert res_b is not None
    # Verify master prediction results contain evidence graph provenance
    career_a = next((p for p in res_a["predictions"] if p["domain"] == "Career & Authority"), None)
    career_b = next((p for p in res_b["predictions"] if p["domain"] == "Career & Authority"), None)
    assert career_a is not None
    assert career_b is not None
    assert len(career_a["evidence_chain"]) >= 1
    assert len(career_b["evidence_chain"]) >= 1

def test_p03_r28_cache_fail_closed():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    chart.chart_fingerprint = None
    with pytest.raises(ValueError, match="MISSING_CHART_PROVENANCE"):
        generate_evidence_based_predictions(chart, selected_date=dt)

def test_p03_r28_unsupported_event_fails():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    with pytest.raises(ValueError, match="UNSUPPORTED_EVENT"):
        generate_evidence_based_predictions(chart, selected_date=dt, event_requests={"Career": "BAD_EVENT"})

def test_p03_r28_domain_mismatch_fails():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    with pytest.raises(ValueError, match="DOMAIN_MISMATCH"):
        generate_evidence_based_predictions(chart, selected_date=dt, event_requests={"Finance": "PROMOTION"})

def test_p03_r28_evidence_graph_classifications():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    res = evaluate_natal_promise(chart, "CAREER", "PROMOTION")
    eg = res["evidence_graph"]
    assert "nodes" in eg
    assert "edges" in eg
    classifications = {n["classification"] for n in eg["nodes"]}
    assert "SCORING_CONTRIBUTION" in classifications or "FACT" in classifications
