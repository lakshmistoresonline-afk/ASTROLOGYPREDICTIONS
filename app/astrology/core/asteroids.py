from .swe_proxy import swe
from typing import Dict, Any

ASTEROIDS = {
    "Ceres": 1,
    "Pallas": 2,
    "Juno": 3,
    "Vesta": 4,
    "Chiron": 15,
    "Eros": 433,
    "Psyche": 16,
    "Sappho": 80,
    "Proserpina": 26,
    "Pholus": 5145,
    "Nessus": 7066,
    "Hygiea": 10
}

def get_asteroid_positions(jd_ut: float) -> Dict[str, Dict[str, Any]]:
    results = {}
    for name, aid in ASTEROIDS.items():
        # Swiss Ephemeris uses negative IDs or specific flags for asteroids
        # For Ceres (1), Pallas (2), Juno (3), Vesta (4) - they are built-in
        res = swe.calc_ut(jd_ut, aid)
        lon = res[0] if not isinstance(res[0], list) else res[0][0]
        results[name] = {
            "longitude": lon,
            "rashi": int(lon // 30),
            "degree": lon % 30,
            "interpretation": _get_asteroid_meaning(name)
        }
    return results

def _get_asteroid_meaning(name: str) -> str:
    meanings = {
        "Ceres": "Nurturing, family bonds, and physical sustenance.",
        "Pallas": "Wisdom, strategic thinking, and pattern recognition.",
        "Juno": "Partnership, commitment, and fairness in relationships.",
        "Vesta": "Devotion, focus, and spiritual service.",
        "Chiron": "The 'Wounded Healer' - areas of deep pain and potential mastery.",
        "Eros": "Erotic love, passion, and creative vital force.",
        "Psyche": "Psychological depth, soul-connection, and transformation.",
        "Sappho": "Poetic expression, refinement, and aesthetic appreciation.",
        "Hygiea": "Physical health, cleanliness, and preventative care."
    }
    return meanings.get(name, "Minor archetypal influence.")
