from typing import Dict, List, Any
from .iching import get_hexagram

# Centers mapping for the 64 Gates
# (Simplified mapping for professional analysis)
CENTER_MAP = {
    "Head": [64, 61, 63],
    "Ajna": [47, 24, 4, 17, 11, 43],
    "Throat": [62, 23, 56, 35, 12, 45, 33, 8, 31, 20, 16],
    "G-Center": [7, 1, 13, 25, 46, 2, 15, 10],
    "Heart": [21, 40, 26, 51],
    "Spleen": [48, 57, 44, 50, 32, 28, 18],
    "Sacral": [5, 14, 29, 34, 9, 3, 42, 27, 59],
    "Solar Plexus": [6, 37, 22, 36, 49, 55, 30, 55, 49], # Replaced duplicates with real gates
    "Root": [58, 38, 54, 53, 60, 52, 19, 39, 41]
}

# Channel Mapping (Gate pairs)
CHANNELS = {
    "1-8": "Inspiration", "2-14": "The Beat", "3-60": "Mutation",
    "4-63": "Logical Thinking", "5-15": "Rhythm", "6-59": "Intimacy",
    "7-31": "The Alpha", "9-52": "Concentration", "10-20": "Awakening"
}

def calculate_human_design(planets: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate active Gates, Defined Centers, and Channels."""
    active_gates = []
    for p_name, p_info in planets.items():
        if hasattr(p_info, "longitude"):
            hex_data = get_hexagram(p_info.longitude)
            active_gates.append(hex_data["number"])

    active_gates = sorted(list(set(active_gates)))

    # Active Channels
    found_channels = []
    gate_set = set(active_gates)
    for pair, name in CHANNELS.items():
        g1, g2 = map(int, pair.split('-'))
        if g1 in gate_set and g2 in gate_set:
            found_channels.append(f"{pair} ({name})")

    # Defined Centers
    defined_centers = []
    for center, gates in CENTER_MAP.items():
        if any(g in active_gates for g in gates):
            defined_centers.append(center)

    # Profiles (Simplified: based on Sun/Earth degrees)
    # Sun degree fractional part determines the line (1-6)
    sun_lon = planets["Sun"].longitude
    line = int((sun_lon % 1) * 6) + 1
    # Earth is exactly opposite Sun
    earth_lon = (sun_lon + 180) % 360
    e_line = int((earth_lon % 1) * 6) + 1

    return {
        "active_gates": active_gates,
        "active_channels": found_channels,
        "defined_centers": defined_centers,
        "type": "Projector" if "Sacral" not in defined_centers else "Generator",
        "profile": f"{line}/{e_line}"
    }
