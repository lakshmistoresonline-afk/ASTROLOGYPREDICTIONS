from typing import Dict, List, Any

def calculate_midpoints(planets: Dict[str, Any]) -> Dict[str, float]:
    """Calculate all planetary midpoints (A/B)."""
    p_names = list(planets.keys())
    results = {}

    for i in range(len(p_names)):
        for j in range(i + 1, len(p_names)):
            p1_name = p_names[i]
            p2_name = p_names[j]
            p1_lon = getattr(planets[p1_name], "longitude", 0)
            p2_lon = getattr(planets[p2_name], "longitude", 0)

            # Midpoint formula (Shortest distance)
            diff = (p1_lon - p2_lon + 360) % 360
            if diff > 180:
                mid = (p1_lon + (360 - diff) / 2) % 360
            else:
                mid = (p2_lon + diff / 2) % 360

            results[f"{p1_name}/{p2_name}"] = mid

    return results

def get_midpoint_structures(planets: Dict[str, Any], midpoints: Dict[str, float]) -> List[str]:
    """Check if any planet occupies a midpoint (C = A/B)."""
    structures = []
    for p_name, p_info in planets.items():
        p_lon = getattr(p_info, "longitude", 0)
        for m_name, m_lon in midpoints.items():
            if abs(p_lon - m_lon) < 1.5: # 1.5 degree orb
                structures.append(f"{p_name} = {m_name}: Significant structural point for {p_name}'s expression.")
    return structures
