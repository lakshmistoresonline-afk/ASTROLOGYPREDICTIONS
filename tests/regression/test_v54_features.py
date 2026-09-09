import pytest
from app.astrology.predictions.v54_signatures import get_event_signature
from app.astrology.predictions.v54_ablation import run_counterfactual_ablation

def test_event_signature_library():
    sig = get_event_signature("promotion")
    assert sig["domain"] == "CAREER"
    assert "Sun" in sig["primary_significators"]

    gen_sig = get_event_signature("unknown_event")
    assert gen_sig["domain"] == "GENERAL"

def test_counterfactual_ablation():
    ctx = {"score": 80.0}
    res = run_counterfactual_ablation(ctx, ["NATAL", "DASHA"])
    assert res["effective_score"] == 35.0
    assert res["state"] == "WITHHELD"
