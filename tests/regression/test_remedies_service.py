import pytest
from datetime import datetime
from app.astrology.core.chart import calculate_chart_data
from app.services.remedies import VedicRemedialService

def test_vedic_remedial_service():
    dt = datetime(1990, 9, 10, 14, 30)
    lat = 28.6139
    lon = 77.2090
    tz = "Asia/Kolkata"

    chart = calculate_chart_data(dt, lat, lon, tz)
    remedies = VedicRemedialService.generate_recommendations(chart)
    assert remedies["ascendant_rashi"] is not None
    assert remedies["recommended_gemstone"] is not None
    assert remedies["vedic_mantra"] is not None
