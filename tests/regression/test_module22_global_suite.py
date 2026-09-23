import pytest
from datetime import datetime
from app.astrology.core.high_latitude_cusps import high_latitude_cusp_engine
from app.astrology.timing.transit_trigger_engine import transit_trigger_engine
from app.astrology.synthesis.contradiction_resolver import contradiction_resolver
from app.astrology.core.calculation_config import calculate_canonical_chart
from app.astrology.predictions.master_synthesizer import master_predictive_synthesizer

def test_module22_high_latitude_polar_births():
    """Validates that high-latitude births (Tromsø 69.6N, Reykjavik 64.1N) compute valid non-overlapping house cusps."""
    jd_ut = 2446702.1875 # 1986-09-28 16:30

    # 1. Tromsø, Norway (69.6821 N, 18.9553 E) - Polar Region
    polar_res = high_latitude_cusp_engine.calculate_houses_polar_safe(jd_ut, 69.6821, 18.9553)
    assert polar_res["is_polar_region"] is True
    assert polar_res["house_system_used"] in ["K", "W", "E"]
    assert len(polar_res["cusps"]) == 12

    # Verify non-overlapping cusps
    cusps = polar_res["cusps"]
    for i in range(12):
        diff = (cusps[(i + 1) % 12] - cusps[i] + 360.0) % 360.0
        assert diff > 0.01

    # 2. Reykjavik, Iceland (64.1466 N, -21.9426 W) - Near Polar
    reyk_res = high_latitude_cusp_engine.calculate_houses_polar_safe(jd_ut, 64.1466, -21.9426)
    assert len(reyk_res["cusps"]) == 12

def test_module22_micro_transit_crossover_triggers():
    """Verifies that exact orbital crossovers (<= 0 deg 15 min = 0.25 deg) generate micro-triggers."""
    transit_planets = {"Jupiter": 161.25} # Jupiter at 161.25 deg
    natal_points = {"Sun": 161.35}         # Sun at 161.35 deg (orb = 0.10 deg = 6.0 arcmin <= 15 arcmin)

    now = datetime(2026, 10, 20, 14, 30)
    triggers = transit_trigger_engine.calculate_micro_triggers(transit_planets, natal_points, now, max_orb_arcmin=15.0)

    assert len(triggers) == 1
    assert triggers[0]["transiting_planet"] == "Jupiter"
    assert triggers[0]["natal_point"] == "Sun"
    assert triggers[0]["aspect_type"] == "CONJUNCTION"
    assert triggers[0]["orb_error_arcmin"] == 6.0
    assert 0.5 <= triggers[0]["intensity_score"] <= 1.0

def test_module22_contradiction_resolution_matrix():
    """Verifies that conflicting raw signals (e.g. KP unfavorable vs Parashari high) resolve into a single unified verdict."""
    # Case 1: KP Unfavorable (Negates feasibility)
    res1 = contradiction_resolver.resolve_contradictions(
        kp_favorable=False, parashari_score=85.0, jaimini_activated=True, domain="Career", event_type="PROMOTION"
    )
    assert res1["verdict"] == "BLOCKED / DELAYED"
    assert res1["final_harmonized_score"] <= 40.0
    assert res1["has_contradiction"] is True
    assert "BLOCKED or DELAYED" in res1["harmonized_narrative"]

    # Case 2: KP Favorable + Jaimini Confirmation Boost
    res2 = contradiction_resolver.resolve_contradictions(
        kp_favorable=True, parashari_score=70.0, jaimini_activated=True, domain="Career", event_type="PROMOTION"
    )
    assert res2["verdict"] == "CONFIRMED_ACTIVE"
    assert res2["final_harmonized_score"] == 87.5 # 70.0 * 1.25
    assert res2["has_contradiction"] is False

def test_module22_end_to_end_sub_150ms_pipeline():
    """End-to-end pipeline execution time test ensuring sub-150ms execution speed."""
    import time
    dt = datetime(1986, 9, 28, 16, 30)
    chart = calculate_canonical_chart(dt, 10.7867, 76.6548, "Asia/Kolkata")

    start = time.time()
    master_report = master_predictive_synthesizer.synthesize_master_prediction(
        chart_obj=chart, target_domain="Career & Authority", target_event="PROMOTION", selected_date=datetime(2026, 10, 20)
    )
    elapsed_ms = (time.time() - start) * 1000.0

    assert master_report.zero_null_verified is True
    assert elapsed_ms < 150.0 # Sub-150ms execution performance invariant
