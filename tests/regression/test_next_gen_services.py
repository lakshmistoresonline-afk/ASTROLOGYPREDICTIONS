import pytest
from datetime import datetime
from app.astrology.core.chart import calculate_chart_data
from app.services.transit_alert_service import TransitAlertService
from app.services.panchang_service import PanchangService

def test_transit_alert_service():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_chart_data(dt, 28.6139, 77.2090, "Asia/Kolkata")
    forecast = TransitAlertService.generate_weather_forecast(chart, datetime(2026, 6, 1))
    assert forecast["forecast_date"] is not None
    assert "overall_weather" in forecast
    assert isinstance(forecast["active_alerts"], list)

def test_panchang_service():
    dt = datetime(2026, 6, 1, 10, 0)
    p = PanchangService.get_daily_panchang(dt, 28.6139, 77.2090, "Asia/Kolkata")
    assert p["date"] is not None
    assert p["tithi"] is not None
    assert p["nakshatra"] is not None
