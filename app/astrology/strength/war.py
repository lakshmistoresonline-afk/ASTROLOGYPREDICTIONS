from typing import Dict, List, Any

def analyze_planetary_war(planets: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Graha Yuddha (Planetary War):
    Occurs when two planets from Mars, Mercury, Jupiter, Venus, Saturn
    are within 1 degree of each other.
    Rule: Planet with LOWER longitude wins (gets strong).
    Exceptions: Venus usually wins regardless.
    """
    warriors = ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    results = []

    p_names = list(planets.keys())
    for i in range(len(p_names)):
        for j in range(i + 1, len(p_names)):
            p1_name, p2_name = p_names[i], p_names[j]
            if p1_name not in warriors or p2_name not in warriors: continue

            p1, p2 = planets[p1_name], planets[p2_name]
            diff = abs(p1.longitude - p2.longitude)
            if diff > 180: diff = 360 - diff

            if diff < 1.0:
                # War detected
                # Standard Winner: lower longitude
                if p1_name == "Venus" or p2_name == "Venus":
                    winner = "Venus"
                    loser = p1_name if p2_name == "Venus" else p2_name
                else:
                    winner = p1_name if p1.longitude < p2.longitude else p2_name
                    loser = p2_name if winner == p1_name else p1_name

                results.append({
                    "planets": [p1_name, p2_name],
                    "winner": winner,
                    "loser": loser,
                    "distance": round(diff, 2),
                    "impact": f"{winner} wins the Graha Yuddha, becoming significantly empowered, while {loser} is defeated."
                })

    return results
