import pytest
from datetime import datetime
from app.astrology.core.calculation_config import calculate_canonical_chart
from app.astrology.astrocartography import astrocartography_engine

def test_astrocartography_geojson_line_generation():
    dt = datetime(1986, 9, 28, 16, 30)
    chart = calculate_canonical_chart(dt, 10.7867, 76.6548, "Asia/Kolkata")

    geojson = astrocartography_engine.generate_planetary_lines_geojson(chart.planets)

    assert geojson["type"] == "FeatureCollection"
    assert len(geojson["features"]) >= 14 # MC and IC lines for 7 planets
    assert geojson["features"][0]["geometry"]["type"] == "LineString"
    assert "MC" in geojson["features"][0]["properties"]["line_type"]

def test_astrocartography_relocation_report():
    dt = datetime(1986, 9, 28, 16, 30)
    chart = calculate_canonical_chart(dt, 10.7867, 76.6548, "Asia/Kolkata")

    # Relocate from Palakkad, India to London, UK (51.5074 N, -0.1278 W)
    reloc_res = astrocartography_engine.evaluate_relocation_chart(
        chart, "London, UK", 51.5074, -0.1278
    )

    assert reloc_res["target_city"] == "London, UK"
    assert "relocated_ascendant" in reloc_res
    assert len(reloc_res["shifted_planets"]) >= 7
