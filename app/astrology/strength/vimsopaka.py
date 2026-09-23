from typing import Dict, Any, List

def calculate_vimsopaka_bala(chart: Any) -> Dict[str, float]:
    """
    Calculates Vimsopaka Bala (strength in divisional charts).
    Dasa-Varga (10 divisions) or Shodasa-Varga (16 divisions).
    Uses points assigned to each varga.
    """
    # Weights for Shodasa-Varga (Total 20 points)
    WEIGHTS = {
        "D1": 3.5, "D2": 1.0, "D3": 1.0, "D4": 1.5, "D7": 1.5,
        "D9": 3.0, "D10": 1.5, "D12": 1.0, "D16": 1.0, "D20": 0.5,
        "D24": 0.5, "D27": 0.5, "D30": 1.0, "D40": 0.5, "D45": 0.5, "D60": 1.0
    }

    planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    results = {}

    from .dignity import get_dignity

    for p in planets:
        total_points = 0.0
        # For each varga, check dignity
        for varga_name, weight in WEIGHTS.items():
            varga_positions = chart.divisional_charts.get(varga_name)
            if not varga_positions: continue

            r_idx = varga_positions.get(p)
            if r_idx is None: continue

            # Varga charts in Jyotish OS only store rashi index.
            # We assume 0 degrees within that rashi for dignity check (Standard practice)
            dignity = get_dignity(p, r_idx, 0.0)

            pts = 7 # Default Neutral
            if "Exalted" in dignity: pts = 20
            elif "Moolatrikona" in dignity: pts = 18
            elif "Own Sign" in dignity: pts = 15
            elif "Great Friend" in dignity: pts = 12
            elif "Friend" in dignity: pts = 10
            elif "Neutral" in dignity: pts = 7
            elif "Enemy" in dignity: pts = 4
            elif "Great Enemy" in dignity: pts = 2
            elif "Debilitated" in dignity: pts = 1

            total_points += (pts * weight)

        # Normalize to 20-point scale (Sum of weights is 20)
        results[p] = round(total_points / 20.0, 2)

    return results
