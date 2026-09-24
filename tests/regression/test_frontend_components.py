import pytest
import os

def test_frontend_components_files_exist():
    files = [
        "frontend/src/types/chart.ts",
        "frontend/src/components/NatalWheel.tsx",
        "frontend/src/components/PlanetInspector.tsx",
        "frontend/src/hooks/useAstrologyChart.ts"
    ]

    for f in files:
        full_path = os.path.abspath(f)
        assert os.path.exists(full_path), f"File {f} is missing!"
        assert os.path.getsize(full_path) > 100, f"File {f} is empty or incomplete!"

def test_frontend_chart_types_spec_content():
    with open("frontend/src/types/chart.ts", "r", encoding="utf-8") as f:
        content = f.read()

    assert "export interface PlanetPosition" in content
    assert "export interface HouseCusp" in content
    assert "export interface AspectLine" in content
    assert "export interface ChartDataPayload" in content
    assert "functionalPowerPct: number" in content

def test_frontend_natal_wheel_spec_content():
    with open("frontend/src/components/NatalWheel.tsx", "r", encoding="utf-8") as f:
        content = f.read()

    assert "export const NatalWheel" in content
    assert "degreeToPolar" in content
    assert "hoveredPlanet" in content
    assert "selectedPlanetId" in content
    assert "amberGlow" in content

def test_frontend_planet_inspector_spec_content():
    with open("frontend/src/components/PlanetInspector.tsx", "r", encoding="utf-8") as f:
        content = f.read()

    assert "export const PlanetInspector" in content
    assert "functionalPowerPct" in content
    assert "Rx" in content
    assert "powerColor" in content

def test_frontend_use_astrology_chart_hook_spec_content():
    with open("frontend/src/hooks/useAstrologyChart.ts", "r", encoding="utf-8") as f:
        content = f.read()

    assert "export const useAstrologyChart" in content
    assert "fetchChart" in content
    assert "apiEndpoint" in content
    assert "ChartDataPayload" in content
