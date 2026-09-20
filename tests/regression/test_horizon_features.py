import pytest
from datetime import datetime
from app.astrology.core.chart import calculate_chart_data
from app.services.yoga_scanner import YogaScannerService
from app.services.career_profiler import VocationalCareerProfiler
from app.services.calendar_export_service import AstrologicalCalendarExportService

def test_yoga_scanner_service():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_chart_data(dt, 28.6139, 77.2090, "Asia/Kolkata")
    res = YogaScannerService.scan_yogas(chart)
    assert "detected_yogas" in res
    assert isinstance(res["detected_yogas"], list)

def test_career_profiler_service():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_chart_data(dt, 28.6139, 77.2090, "Asia/Kolkata")
    res = VocationalCareerProfiler.profile_career(chart)
    assert "recommended_primary_industry" in res

def test_calendar_export_service():
    events = [{"summary": "Jupiter Transit Peak", "date": "2026-06-01T10:00:00Z", "description": "Favorable alignment"}]
    ical = AstrologicalCalendarExportService.generate_ical_feed(events)
    assert "BEGIN:VCALENDAR" in ical
    assert "SUMMARY:Jupiter Transit Peak" in ical
    assert "END:VCALENDAR" in ical
