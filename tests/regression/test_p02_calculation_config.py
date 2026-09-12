import pytest
from app.astrology.core.calculation_config import (
    CalculationConfig,
    get_canonical_calculation_config,
    generate_chart_fingerprint,
    validate_chart_geometry
)

def test_p02_config_immutability():
    cfg = get_canonical_calculation_config()
    with pytest.raises(Exception):
        cfg.ayanamsa = "Raman"

def test_p02_fingerprint_determinism_and_precision():
    fp1 = generate_chart_fingerprint("1990-09-10T09:00:00Z", 28.613912, 77.209015, "Asia/Kolkata")
    fp2 = generate_chart_fingerprint("1990-09-10T09:00:00Z", 28.613913, 77.209016, "Asia/Kolkata")
    fp3 = generate_chart_fingerprint("1990-09-10T09:00:00Z", 28.613912, 77.209015, "Asia/Kolkata")
    assert fp1 == fp3

def test_p02_chart_geometry_validator():
    valid_chart = {"ascendant": 0.0, "planets": {"Sun": {"house": 1, "rashi": 0}, "Moon": {"house": 4, "rashi": 3}}}
    assert validate_chart_geometry(valid_chart) is True

    invalid_chart = {"ascendant": 0.0, "planets": {"Sun": {"house": 15}}}
    with pytest.raises(ValueError):
        validate_chart_geometry(invalid_chart)
