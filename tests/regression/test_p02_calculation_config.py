import pytest
from app.astrology.core.calculation_config import CANONICAL_CALCULATION_CONFIG, generate_chart_fingerprint

def test_p02_fingerprint_determinism():
    fp1 = generate_chart_fingerprint("1990-09-10T09:00:00Z", 28.6139, 77.2090, "Asia/Kolkata")
    fp2 = generate_chart_fingerprint("1990-09-10T09:00:00Z", 28.6139, 77.2090, "Asia/Kolkata")
    assert fp1 == fp2

def test_p02_fingerprint_sensitivity():
    fp1 = generate_chart_fingerprint("1990-09-10T09:00:00Z", 28.6139, 77.2090, "Asia/Kolkata")
    fp2 = generate_chart_fingerprint("1990-09-10T09:01:00Z", 28.6139, 77.2090, "Asia/Kolkata")
    assert fp1 != fp2
