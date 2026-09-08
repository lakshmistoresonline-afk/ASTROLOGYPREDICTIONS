import pytest
from datetime import datetime, timedelta
from app.astrology.core.chart import calculate_chart_data

def test_sign_boundaries():
    """Test planets very close to sign boundaries (0° and 29.99°)."""
    # 2024-03-20 12:00 UTC - Sun is near 0° Aries
    dt = datetime(2024, 3, 20, 12, 0)
    lat, lon = 0.0, 0.0
    tz = "UTC"

    chart = calculate_chart_data(dt, lat, lon, tz)
    sun_lon = chart.planets["Sun"].longitude
    sun_rashi = chart.planets["Sun"].rashi

    # Sidereal Sun on March 20 is around 6° Pisces (Meena) usually
    # (Lahiri ayanamsa is ~24°)
    # Let's find a date where a planet is exactly at a boundary.
    # For now, we just ensure the calculation doesn't crash and returns valid rashi [0, 11]

    for p_name, p_info in chart.planets.items():
        assert 0 <= p_info.rashi <= 11
        assert 0 <= p_info.degree < 30
        # Precision check: degree = longitude % 30
        assert abs(p_info.degree - (p_info.longitude % 30)) < 0.0001

def test_midnight_birth():
    """Test birth times exactly at midnight or across day boundaries."""
    # New Year Midnight
    dt1 = datetime(2024, 1, 1, 0, 0)
    dt2 = datetime(2023, 12, 31, 23, 59, 59)
    lat, lon = 28.6, 77.2
    tz = "Asia/Kolkata"

    c1 = calculate_chart_data(dt1, lat, lon, tz)
    c2 = calculate_chart_data(dt2, lat, lon, tz)

    # Positions should be extremely close
    diff = abs(c1.planets["Moon"].longitude - c2.planets["Moon"].longitude)
    assert diff < 0.1 # Moon moves ~0.5° per hour, so ~0.0001° per second

def test_polar_birth():
    """Test calculation at high latitudes (Lagna calculation stability)."""
    dt = datetime(2024, 6, 21, 12, 0) # Solstice
    lat, lon = 65.0, 10.0 # High North (Arctic Circle)
    tz = "UTC"

    # This often fails in simplistic house systems, pyswisseph should handle it.
    chart = calculate_chart_data(dt, lat, lon, tz)
    assert chart.ascendant is not None
    assert 0 <= chart.ascendant < 360
