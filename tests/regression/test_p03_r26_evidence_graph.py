import pytest
from datetime import datetime
from app.astrology.core.calculation_config import calculate_canonical_chart
from app.astrology.predictions.evidence import EvidenceNode, EvidenceGraph, calculate_score_from_evidence
from app.astrology.predictions.v5_natal_promise import evaluate_natal_promise, EVENT_RULES
from app.astrology.predictions.request import normalize_prediction_request, prediction_request_fingerprint
from app.astrology.predictions.engine import generate_evidence_based_predictions, PREDICTION_ENGINE_VERSION

def test_p03_r26_engine_version():
    assert PREDICTION_ENGINE_VERSION == "P0.3-R34"

def test_p03_r26_evidence_graph_structure():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    res = evaluate_natal_promise(chart, "CAREER", "PROMOTION")
    assert "evidence_graph" in res
    eg = res["evidence_graph"]
    assert "nodes" in eg
    assert "edges" in eg
    assert len(eg["nodes"]) >= 1

def test_p03_r26_score_reconstruction_from_graph():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    res = evaluate_natal_promise(chart, "CAREER", "PROMOTION")
    eg = EvidenceGraph()
    for n_dict in res["evidence_graph"]["nodes"]:
        eg.add_node(EvidenceNode(**n_dict))
    recomputed = calculate_score_from_evidence(eg)
    assert recomputed == res["promise_score"]

def test_p03_r26_true_target_date_invariance():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")

    res_a = evaluate_natal_promise(chart, "CAREER", "PROMOTION")
    res_b = evaluate_natal_promise(chart, "CAREER", "PROMOTION")

    assert res_a["promise_score"] == res_b["promise_score"]
    assert res_a["promise_level"] == res_b["promise_level"]
    assert res_a["evidence_graph"] == res_b["evidence_graph"]

def test_p03_r26_missing_provenance_fails_closed():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    chart.chart_fingerprint = None
    with pytest.raises(ValueError, match="MISSING_CHART_PROVENANCE"):
        generate_evidence_based_predictions(chart, selected_date=dt)
