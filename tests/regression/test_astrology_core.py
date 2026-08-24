import pytest
from datetime import datetime
from app.astrology.core.chart import calculate_chart_data

def test_chart_calculation_accuracy():
    """Verify core planetary positions for a known date."""
    # Date: 1990-01-01 12:00 PM IST
    # Location: New Delhi (28.6139N, 77.2090E)
    dt = datetime(1990, 1, 1, 12, 0)
    lat = 28.6139
    lon = 77.2090
    tz = "Asia/Kolkata"

    chart = calculate_chart_data(dt, lat, lon, tz)

    assert chart is not None
    assert "Sun" in chart.planets
    assert "Moon" in chart.planets

    # Sun in Sagittarius (Dhanu) in early Jan
    assert chart.planets["Sun"].rashi == 8 # 8 = Sagittarius (0-indexed)

    # Check Ayanamsa (Lahiri)
    # 1990 Ayanamsa is approx 23.7
    assert 23.0 < chart.ayanamsa < 24.5

    # Check Lagna (Pisces/Meena for 12 PM in Delhi in Jan)
    # Actually at 12 PM in Delhi, Pisces is often rising.
    assert chart.asc_rashi in [10, 11] # Aquarius or Pisces

def test_divisional_charts():
    """Verify D9 and D10 logic."""
    dt = datetime(1990, 1, 1, 12, 0)
    lat = 28.6139
    lon = 77.2090
    tz = "Asia/Kolkata"

    chart = calculate_chart_data(dt, lat, lon, tz)

    assert "D9" in chart.divisional_charts
    assert "D10" in chart.divisional_charts

    d9 = chart.divisional_charts["D9"]
    d10 = chart.divisional_charts["D10"]

    assert len(d9) >= 8 # Lagna + 7 planets
    assert len(d10) >= 8

def test_varga_integrity():
    """Verify D27 and D30 specific Parashari rules."""
    from app.astrology.charts.divisional import calculate_varga_rashi

    # D30 Trimshamsha: Odd Sign (Aries), 4° -> Mars (Aries=0)
    assert calculate_varga_rashi(4.0, 30) == 0
    # D30 Trimshamsha: Odd Sign (Aries), 8° -> Saturn (Aquarius=10)
    assert calculate_varga_rashi(8.0, 30) == 10

    # D27 Saptavimshamsha: Fire Sign (Aries), 1° -> Aries (0)
    # Span is 1° 6' 40" (1.111°)
    assert calculate_varga_rashi(0.5, 27) == 0
    # Earth Sign (Taurus), 1° -> Capricorn (9)
    assert calculate_varga_rashi(31.0, 27) == 9

def test_shadbala_calculation():
    """Verify Shadbala exists and has reasonable values."""
    dt = datetime(1990, 1, 1, 12, 0)
    lat = 28.6139
    lon = 77.2090
    tz = "Asia/Kolkata"

    chart = calculate_chart_data(dt, lat, lon, tz)

    for p_name, p_info in chart.planets.items():
        if p_name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
            assert p_info.shadbala_score is not None
            assert p_info.shadbala_score > 0
