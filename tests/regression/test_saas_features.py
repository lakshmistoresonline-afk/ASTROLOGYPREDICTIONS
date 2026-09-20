import pytest
from datetime import datetime
from app.astrology.core.chart import calculate_chart_data
from app.services.shadbala_service import ShadbalaService
from app.services.ashtakavarga_service import AshtakavargaTransitService
from app.services.synastry_service import SynastryCompatibilityService

def test_shadbala_service():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_chart_data(dt, 28.6139, 77.2090, "Asia/Kolkata")
    res = ShadbalaService.calculate_shadbala(chart)
    assert "planet_strengths" in res
    assert "Sun" in res["planet_strengths"]

def test_ashtakavarga_service():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_chart_data(dt, 28.6139, 77.2090, "Asia/Kolkata")
    res = AshtakavargaTransitService.calculate_transit_heatmap(chart)
    assert "sarvashtakavarga_bindus" in res
    assert len(res["sarvashtakavarga_bindus"]) == 12

def test_synastry_service():
    dt1 = datetime(1990, 9, 10, 14, 30)
    dt2 = datetime(1992, 5, 15, 10, 0)
    chart1 = calculate_chart_data(dt1, 28.6139, 77.2090, "Asia/Kolkata")
    chart2 = calculate_chart_data(dt2, 19.0760, 72.8777, "Asia/Kolkata")
    res = SynastryCompatibilityService.evaluate_compatibility(chart1, chart2)
    assert "guna_milan_score" in res
    assert "compatibility_percentage" in res
