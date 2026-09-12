import pytest
from datetime import datetime
from app.astrology.core.calculation_config import (
    CalculationConfig,
    get_canonical_calculation_config,
    generate_chart_fingerprint,
    validate_chart_geometry,
    validate_config_against_v315_engine,
    calculate_canonical_chart
)

def test_p02_config_immutability():
    cfg = get_canonical_calculation_config()
    with pytest.raises(Exception):
        cfg.ayanamsa = "Raman"

def test_p02_config_mutation_rejection():
    cfg_bad_zodiac = CalculationConfig(zodiac="TROPICAL")
    with pytest.raises(ValueError, match="CONFIG_INCOMPATIBLE"):
        validate_config_against_v315_engine(cfg_bad_zodiac)

    cfg_bad_ayanamsa = CalculationConfig(ayanamsa="RAMAN")
    with pytest.raises(ValueError, match="CONFIG_INCOMPATIBLE"):
        validate_config_against_v315_engine(cfg_bad_ayanamsa)

    cfg_bad_node = CalculationConfig(node_mode="TRUE")
    with pytest.raises(ValueError, match="CONFIG_INCOMPATIBLE"):
        validate_config_against_v315_engine(cfg_bad_node)

def test_p02_fingerprint_determinism_and_precision():
    fp1 = generate_chart_fingerprint("1990-09-10T09:00:00Z", 28.613912, 77.209015, "Asia/Kolkata")
    fp3 = generate_chart_fingerprint("1990-09-10T09:00:00Z", 28.613912, 77.209015, "Asia/Kolkata")
    assert fp1 == fp3

def test_p02_chart_geometry_validator():
    valid_chart = {"ascendant": 0.0, "houses": [1,2,3,4,5,6,7,8,9,10,11,12], "planets": {"Sun": {"house": 1, "rashi": 0}, "Moon": {"house": 4, "rashi": 3}}}
    assert validate_chart_geometry(valid_chart) is True

    invalid_chart = {"ascendant": 0.0, "planets": {"Sun": {"house": 15}}}
    with pytest.raises(ValueError):
        validate_chart_geometry(invalid_chart)

def test_p02_runtime_canonical_chart():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_canonical_chart(dt, 10.5276, 76.2144, "Asia/Kolkata")
    assert chart is not None
    assert chart.calculation_config is not None
    assert chart.calculation_provenance is not None
    assert chart.chart_fingerprint is not None
    assert chart.calculation_config_fingerprint is not None
    assert chart.astronomical_house_system == "PLACIDUS"
    assert chart.interpretive_house_system == "WHOLE_SIGN"

def test_p02_whole_sign_vs_placidus_divergence():
    cfg = get_canonical_calculation_config()
    assert cfg.interpretive_house_system == "WHOLE_SIGN"
    assert cfg.astronomical_house_system == "PLACIDUS"

def test_p02_dict_vs_chart_validation_parity():
    valid_dict = {"ascendant": 0.0, "houses": [1,2,3,4,5,6,7,8,9,10,11,12], "planets": {"Sun": {"house": 1, "rashi": 0}}}
    assert validate_chart_geometry(valid_dict) is True

    invalid_dict = {"ascendant": 0.0, "houses": [1], "planets": {"Sun": {"house": 1, "rashi": 0}}}
    with pytest.raises(ValueError):
        validate_chart_geometry(invalid_dict)
