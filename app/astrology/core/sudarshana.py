from typing import Dict, List, Any

def get_sudarshana_analysis(chart: Any) -> Dict[str, Any]:
    """
    Sudarshana Chakra Analysis:
    Combines perspective from Lagna, Moon, and Sun.
    If a house is strong from all three, results are definitive.
    """
    planets = chart.planets
    asc_rashi = chart.asc_rashi
    moon_rashi = planets["Moon"].rashi
    sun_rashi = planets["Sun"].rashi

    house_lords = chart.house_lords

    results = {}

    for h in range(1, 13):
        # 1. From Lagna
        r1 = (asc_rashi + h - 1) % 12
        # 2. From Moon
        r2 = (moon_rashi + h - 1) % 12
        # 3. From Sun
        r3 = (sun_rashi + h - 1) % 12

        # Check occupants
        occ1 = [p for p, info in planets.items() if info.rashi == r1]
        occ2 = [p for p, info in planets.items() if info.rashi == r2]
        occ3 = [p for p, info in planets.items() if info.rashi == r3]

        # Power Score (Simplified: Benefics in all 3 houses?)
        benefics = ["Jupiter", "Venus", "Mercury", "Moon"]
        total_benefics = sum(1 for p in (occ1 + occ2 + occ3) if p in benefics)

        results[h] = {
            "rashis": [r1, r2, r3],
            "occupants": {"Lagna": occ1, "Moon": occ2, "Sun": occ3},
            "total_benefics": total_benefics,
            "resonance": "HIGH" if total_benefics >= 3 else "MEDIUM" if total_benefics >= 1 else "LOW"
        }

    return results
