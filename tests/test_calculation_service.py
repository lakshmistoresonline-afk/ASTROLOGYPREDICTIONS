import pytest
from app.astrology.core.calc_client import calc_client
from datetime import datetime

def test_service_health():
    """Verify calculation service is reachable."""
    assert calc_client.check_health() is True

def test_natal_calculation_integrity():
    """Cross-validate deterministic facts for a known reference chart."""
    # Reference: 1990-01-01 12:00 PM UTC (Delhi approx)
    # Sun should be in Sagittarius (~256 deg)

    facts = calc_client.get_natal_chart(1990, 1, 1, 12.0, 28.6, 77.2)

    assert "planets" in facts
    assert "Sun" in facts["planets"]

    sun_lon = facts["planets"]["Sun"]["longitude"]
    # 256.7 deg is approx Sagittarius 16 deg (Sidereal Lahiri)
    assert 250.0 < sun_lon < 265.0

    assert "ayanamsa" in facts
    assert 23.0 < facts["ayanamsa"] < 24.5

    assert "ascendant" in facts

def test_ketu_opposite_rahu():
    """Verify Ketu is mathematically opposite Rahu."""
    facts = calc_client.get_natal_chart(2024, 8, 28, 10.0, 28.6, 77.2)
    rahu = facts["planets"]["Rahu"]["longitude"]
    ketu = facts["planets"]["Ketu"]["longitude"]

    diff = abs(rahu - ketu)
    # Must be 180 deg or 540 deg etc.
    assert abs(diff - 180.0) < 0.0001 or abs(diff - 180.0) > 359.9999
