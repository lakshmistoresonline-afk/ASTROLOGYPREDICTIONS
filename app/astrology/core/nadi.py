from typing import Dict, List, Any

def get_nadi_connections(planets: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    Bhrigu Nandi Nadi connections based on Sign Triads.
    Dharma: 1, 5, 9 signs.
    Artha: 2, 6, 10 signs.
    Kama: 3, 7, 11 signs.
    Moksha: 4, 8, 12 signs.
    """
    groups = {
        "Dharma": [0, 4, 8],
        "Artha": [1, 5, 9],
        "Kama": [2, 6, 10],
        "Moksha": [3, 7, 11]
    }

    connections = {p: [] for p in planets}

    for name, data in planets.items():
        r = data.rashi
        # Find which group this planet belongs to
        group_name = None
        for g, signs in groups.items():
            if r in signs:
                group_name = g
                break

        if not group_name: continue

        # Connect to all other planets in the SAME group
        for other_name, other_data in planets.items():
            if other_name == name: continue
            if other_data.rashi in groups[group_name]:
                connections[name].append(other_name)

        # 2nd and 12th connections (Planet in next or previous sign)
        for other_name, other_data in planets.items():
            if other_name == name: continue
            if other_data.rashi == (r + 1) % 12:
                connections[name].append(f"{other_name} (2nd)")
            if other_data.rashi == (r - 1 + 12) % 12:
                connections[name].append(f"{other_name} (12th)")

        # 7th connection (Opposition)
        for other_name, other_data in planets.items():
            if other_name == name: continue
            if other_data.rashi == (r + 6) % 12:
                connections[name].append(f"{other_name} (7th)")

    return connections
