import pytest
from datetime import datetime
from app.astrology.core.calculation_config import calculate_canonical_chart
from app.astrology.performance.swisseph_fast_worker import swisseph_fast_worker
from app.astrology.performance.distributed_cache import distributed_cache_manager
from app.astrology.evaluation.hallucination_drift_detector import hallucination_drift_detector
from app.astrology.evaluation.governance_dashboard import governance_dashboard

def test_module15_swisseph_fast_worker():
    jd_ut = 2446702.1875 # Julian day for 1986-09-28 16:30
    positions = swisseph_fast_worker.calculate_fast_planetary_positions(jd_ut)
    assert "Sun" in positions
    assert "Moon" in positions
    assert "Rahu" in positions
    assert "Ketu" in positions
    assert 0.0 <= positions["Sun"] <= 360.0

def test_module15_distributed_cache_region_routing():
    # Palakkad, India (lat 10.78, lon 76.65) -> APAC-SOUTH
    region = distributed_cache_manager.get_nearest_region(10.78, 76.65)
    assert region == "APAC-SOUTH"

    key = "chart-subramanian"
    distributed_cache_manager.set(key, {"status": "CACHED"}, region=region)
    cached = distributed_cache_manager.get(key, region=region)
    assert cached["status"] == "CACHED"

def test_module16_hallucination_drift_detector():
    dt = datetime(1986, 9, 28, 16, 30)
    chart = calculate_canonical_chart(dt, 10.7867, 76.6548, "Asia/Kolkata")

    # Correct claim: Mars is in House 12
    valid_text = "Your natal chart features Mars in House 12 which provides strong energy."
    v_res = hallucination_drift_detector.verify_narrative_factuality(valid_text, chart)
    assert v_res["has_hallucination"] is False

    # False claim: Mars in House 5 (when Mars is actually in House 12)
    hallucinated_text = "Your natal chart features Mars in House 5 which gives creative talent."
    h_res = hallucination_drift_detector.verify_narrative_factuality(hallucinated_text, chart)
    assert h_res["has_hallucination"] is True
    assert "FACTUAL_HALLUCINATION" in h_res["discrepancies"][0]

def test_module16_governance_dashboard():
    governance_dashboard.record_report_metrics(has_hallucination=False, retry_count=0, cost_usd=0.0025)
    metrics = governance_dashboard.get_dashboard_metrics()

    assert metrics["total_reports_processed"] >= 1
    assert metrics["hallucination_rate_ppm"] == 0.0
    assert metrics["governance_status"] == "HEALTHY"
