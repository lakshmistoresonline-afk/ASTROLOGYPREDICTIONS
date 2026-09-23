"""
Automated Astronomy & Mathematical Invariants Suite (Module 5 - Task 5.1).
Validates SAV == 337 invariant, SBC Vedha verification, and Shadbala boundaries across synthetic chart samples.
"""
import pytest
from datetime import datetime, timedelta
from app.astrology.charts.ashtakavarga import calculate_ashtakavarga, assert_sav_total
from app.astrology.core.sarvatobhadra import check_sbc_transit_impact
from app.astrology.core.calculation_config import calculate_canonical_chart

def test_module5_sav_337_invariant_synthetic_charts():
    """Validates sum(SAV) == 337 across multiple synthetic birth dates."""
    base_dt = datetime(1980, 1, 1, 12, 0)
    for i in range(10): # Test 10 distinct synthetic charts
        test_dt = base_dt + timedelta(days=i * 365)
        chart = calculate_canonical_chart(test_dt, 28.6139, 77.2090, "Asia/Kolkata")

        sav = chart.ashtakavarga["SAV"]
        assert sum(sav) == 337
        assert assert_sav_total(sav) is True

def test_module5_sbc_vedha_isolation():
    """Verifies that clear transit positions do not trigger false positive SBC Vedha flags."""
    # Transit Jupiter (benefic) to Natal Moon (far distance)
    transit_planets = {"Jupiter": 120.0, "Venus": 180.0}
    natal_points = {"Moon": 15.0}

    alerts = check_sbc_transit_impact(transit_planets, natal_points, transiting_planet="Jupiter", target_natal="Moon")
    assert len(alerts) == 0 # Zero false positive obstruction alerts

def test_module5_shadbala_boundary_limits():
    """Verifies that all Shadbala scores are non-negative and non-zero for active planets."""
    dt = datetime(1986, 9, 28, 16, 30)
    chart = calculate_canonical_chart(dt, 10.7867, 76.6548, "Asia/Kolkata")

    for p_name, p in chart.planets.items():
        assert p.shadbala_score >= 0.0
        assert p.effective_shadbala >= 0.0
        assert p.functional_power_multiplier > 0.0
