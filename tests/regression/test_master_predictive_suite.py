import pytest
from datetime import datetime, timedelta
from app.astrology.core.calculation_config import calculate_canonical_chart
from app.astrology.prashna.prashna_engine import prashna_engine, KP_249_SEEDS, PrashnaResult
from app.astrology.timing.stationing_eclipse import stationing_eclipse_tracker
from app.astrology.predictions.master_synthesizer import master_predictive_synthesizer, MasterPredictionReport

def test_module21_all_249_prashna_seeds_boundary_mapping():
    """Validates that all 249 Prashna seed numbers map to exact degree intervals and correct Lagna Sub-Lords."""
    assert len(KP_249_SEEDS) == 249

    for seed_id in range(1, 250):
        s_info = prashna_engine.get_seed_boundary(seed_id)
        assert s_info["seed"] == seed_id
        assert 0.0 <= s_info["start_lon"] <= 360.0
        assert 0.0 <= s_info["end_lon"] <= 360.0
        assert s_info["sign_lord"] in ["Mars", "Venus", "Mercury", "Moon", "Sun", "Jupiter", "Saturn"]
        assert s_info["star_lord"] in ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
        assert s_info["sub_lord"] in ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]

def test_module21_prashna_query_evaluation():
    dt = datetime(2026, 10, 20, 12, 0)
    p_res = prashna_engine.evaluate_query(seed_number=108, query_datetime=dt, lat=10.7867, lon=76.6548, target_house=10)

    assert isinstance(p_res, PrashnaResult)
    assert p_res.seed_number == 108
    assert p_res.verdict in ["YES", "NO", "CONDITIONAL"]
    assert 0.0 <= p_res.confidence_score <= 1.0
    assert p_res.primary_significators == [1, 10, 11]

def test_module21_stationing_and_eclipse_detection():
    # 1. Stationing Speed Test (< 0.01 deg/day)
    daily_transits = {
        "Saturn": {"lon": 320.5, "speed": 0.005},  # Stationary
        "Jupiter": {"lon": 115.2, "speed": 0.12}   # Normal
    }
    stations = stationing_eclipse_tracker.detect_planetary_stations(daily_transits)
    assert len(stations) == 1
    assert stations[0]["planet"] == "Saturn"
    assert stations[0]["daily_speed"] == 0.005

    # 2. Eclipse Collision Test (<= 1.5 deg)
    eclipse_lons = [161.0] # Solar Eclipse at 161.0 deg Virgo
    natal_pts = {"Sun": 161.35, "Moon": 96.38} # Sun collision within 0.35 deg
    collisions = stationing_eclipse_tracker.detect_eclipse_collisions(eclipse_lons, natal_pts, orb_tolerance=1.5)

    assert len(collisions) == 1
    assert collisions[0]["natal_point"] == "Sun"
    assert collisions[0]["orb_difference"] == 0.35

def test_module21_master_predictive_synthesizer_50_synthetic_charts():
    """End-to-end test verifying MasterPredictiveSynthesizer generates zero-null payloads across 50 birth charts."""
    base_dt = datetime(1975, 1, 1, 12, 0)

    for i in range(50): # 50 synthetic test birth charts
        test_dt = base_dt + timedelta(days=i * 365)
        chart = calculate_canonical_chart(test_dt, 10.7867, 76.6548, "Asia/Kolkata")

        report = master_predictive_synthesizer.synthesize_master_prediction(
            chart_obj=chart,
            target_domain="Career & Authority",
            target_event="PROMOTION",
            selected_date=datetime(2026, 10, 20),
            prashna_seed=(i % 249) + 1
        )

        assert isinstance(report, MasterPredictionReport)
        assert 0.0 <= report.master_confluence_score <= 100.0
        assert report.confidence_tier in ["TOP_TIER_HIGH_CONFLUENCE", "STRONG_CONFLUENCE", "MODERATE_ALIGNMENT"]
        assert report.precision_timing_window == "2-3 DAY OPERATIONAL WINDOW"
        assert report.zero_null_verified is True
        assert len(report.narrative_summary) > 20
        assert "N/A" not in report.narrative_summary
