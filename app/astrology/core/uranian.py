from .swe_proxy import swe
from typing import Dict, Any

# Uranian Trans-Neptunian Planets (TNPs)
TNPS = {
    "Cupido": 40,
    "Hades": 41,
    "Zeus": 42,
    "Kronos": 43,
    "Apollon": 44,
    "Admetos": 45,
    "Vulkanus": 46,
    "Poseidon": 47
}

def get_uranian_positions(jd_ut: float) -> Dict[str, Dict[str, Any]]:
    """Calculate positions of the 8 Trans-Neptunian Planets."""
    results = {}
    for name, tid in TNPS.items():
        res = swe.calc_ut(jd_ut, tid)
        # Handle both native list return and mock return
        lon = res[0] if not isinstance(res[0], list) else res[0][0]
        results[name] = {
            "longitude": lon,
            "rashi": int(lon // 30),
            "degree": lon % 30,
            "interpretation": _get_tnp_meaning(name)
        }
    return results

def _get_tnp_meaning(name: str) -> str:
    meanings = {
        "Cupido": "Sociability, family, art, and groups.",
        "Hades": "The past, secrets, antiquity, and transformation through depth.",
        "Zeus": "Creative fire, leadership, and controlled energy.",
        "Kronos": "Authority, mastery, and the 'high' or 'expert' level.",
        "Apollon": "Expansion, science, and the 'many' - extreme growth.",
        "Admetos": "Depth, concentration, and the 'seed' - endurance through stillness.",
        "Vulkanus": "Mighty force, power, and overwhelming strength.",
        "Poseidon": "Spiritual light, clarity, and idealism."
    }
    return meanings.get(name, "")
