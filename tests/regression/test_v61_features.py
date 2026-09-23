import pytest
from datetime import datetime, timezone
from app.utils.pdf_generator import generate_complete_pdf
from app.services.sadhana_tracker import SadhanaTrackerService
from app.astrology.core.chart import normalize_dasha_boundary
from app.api.websocket_transits import calculate_current_transits_realtime
from app.astrology.synthesis.language_localizer import language_localizer

def test_v61_pdf_generator_no_deprecation_warnings():
    data = {
        "profile": {"name": "Test User", "dob": "1986-09-28", "tob": "16:30", "place": "Palakkad", "lat": 10.78, "lon": 76.65, "tz": "Asia/Kolkata"},
        "present": {"predictions": []}
    }
    pdf_bytes = generate_complete_pdf(data)
    assert len(pdf_bytes) > 0

def test_v61_sadhana_tracker_utc_timezone_aware():
    plan = SadhanaTrackerService.get_default_sadhana_plan("Jupiter", "Om Gurave Namah")
    assert plan["started_at"] is not None
    assert "T" in plan["started_at"]

def test_v61_dasha_boundary_seconds_normalization():
    dt1 = datetime(2026, 10, 20, 14, 30, 45)
    norm1 = normalize_dasha_boundary(dt1)
    assert norm1.second == 0
    assert norm1.minute == 31

    dt2 = datetime(2026, 10, 20, 14, 30, 12)
    norm2 = normalize_dasha_boundary(dt2)
    assert norm2.second == 0
    assert norm2.minute == 30

def test_v61_websocket_realtime_transits_payload():
    payload = calculate_current_transits_realtime()
    assert payload["stream_event"] == "LIVE_TRANSIT_UPDATE"
    assert "transits" in payload
    assert "Sun" in payload["transits"]
    assert "Moon" in payload["transits"]

def test_v61_multilanguage_localizer():
    term_hi = language_localizer.localize_term("Mahadasha", "hi")
    assert "महादशा" in term_hi

    term_es = language_localizer.localize_term("Lagnavanga", "es")
    assert "Lagna" in term_es

    prompt = language_localizer.localize_narrative_prompt("Report Context", "hi")
    assert "Hindi" in prompt
