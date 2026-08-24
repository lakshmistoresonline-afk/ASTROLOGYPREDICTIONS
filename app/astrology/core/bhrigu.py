from typing import Dict, List, Any

# Bhrigu Bindu: Midpoint between Rahu and Moon
# Rahu-Moon midpoint is a sensitive point for destiny/fame.
def calculate_bhrigu_bindu(moon_lon: float, rahu_lon: float) -> float:
    # Handle Rahu/Ketu as Nodes (usually Rahu is the starting point)
    diff = (moon_lon - rahu_lon + 360) % 360
    return (rahu_lon + diff / 2) % 360

# Bhrigu Phala Logic (Simplified)
# Planet in House descriptions from Bhrigu Samhita
BHRIGU_H_PHALA = {
    "Sun": {
        1: "Courageous, healthy, but may have ego challenges or eye issues.",
        2: "Wealthy, but potential for family disputes or facial marks.",
        10: "High status, government authority, success in professional life."
    },
    "Jupiter": {
        1: "Wise, long-lived, respected, and physically attractive.",
        5: "Highly intelligent, blessed with good children and creative success.",
        9: "Fortunate, spiritual, respected by teachers and society."
    }
    # ... expand as needed
}

def get_bhrigu_insights(planets: Dict[str, Any]) -> List[str]:
    insights = []
    for p_name, p_info in planets.items():
        if p_name in BHRIGU_H_PHALA:
            h = getattr(p_info, "house", None)
            if h in BHRIGU_H_PHALA[p_name]:
                insights.append(f"Bhrigu: {p_name} in H{h} - {BHRIGU_H_PHALA[p_name][h]}")
    return insights
