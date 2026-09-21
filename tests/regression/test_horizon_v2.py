import pytest
from datetime import datetime
from app.astrology.core.chart import calculate_chart_data
from app.services.varshaphala_service import VarshaphalaEngine
from app.services.drishti_service import DrishtiAspectService
from app.services.sadhana_tracker import SadhanaTrackerService

def test_varshaphala_engine():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_chart_data(dt, 28.6139, 77.2090, "Asia/Kolkata")
    res = VarshaphalaEngine.calculate_varshaphala(chart, 2026)
    assert res["target_year"] == 2026
    assert res["muntha_house"] is not None

def test_drishti_service():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_chart_data(dt, 28.6139, 77.2090, "Asia/Kolkata")
    aspects = DrishtiAspectService.calculate_aspects(chart)
    assert isinstance(aspects, list)
    assert len(aspects) > 0

def test_sadhana_tracker():
    plan = SadhanaTrackerService.get_default_sadhana_plan("Jupiter", "Om Brim Brihaspataye Namah")
    assert plan["planet"] == "Jupiter"
    assert plan["target_japam_count"] == 10008
