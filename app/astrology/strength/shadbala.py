from typing import Dict, Any, List
from .dignity import EXALTATION, DEBILITATION, OWN_SIGN, MOOLATRIKONA
from .friendship import NATURAL_FRIENDSHIP, get_compound_friendship
from ..core.houses import RASHI_LORDS

# Dig Bala (Directional Strength)
DIG_BALA_MAP = {
    "Sun": 10, "Mars": 10,
    "Jupiter": 1, "Mercury": 1,
    "Moon": 4, "Venus": 4,
    "Saturn": 7
}

# Kendra-adi Bala
KENDRA_ADI_SCORES = {
    "Kendra": 60,   # 1, 4, 7, 10
    "Panapara": 30, # 2, 5, 8, 11
    "Apoklima": 15  # 3, 6, 9, 12
}

# Sapta-varga-ja Bala points
VargaPoints = {
    "Exalted": 60,
    "Moolatrikona": 45,
    "Own Sign": 30,
    "Great Friend": 20,
    "Friend": 15,
    "Neutral": 10,
    "Enemy": 4,
    "Great Enemy": 2,
}

def calculate_exaltation_bala(planet: str, longitude: float) -> float:
    """Calculate Exaltation Bala (0-60 Virupas)."""
    if planet not in EXALTATION:
        return 0.0
    ex_rashi, ex_deg = EXALTATION[planet]
    ex_lon = ex_rashi * 30 + ex_deg
    db_rashi, db_deg = DEBILITATION[planet]
    db_lon = db_rashi * 30 + db_deg
    diff = (longitude - db_lon) % 360
    if diff > 180: diff = 360 - diff
    return (diff / 180.0) * 60.0

def calculate_dig_bala(planet: str, house: int) -> float:
    """Calculate Dig Bala (0-60 Virupas)."""
    if planet not in DIG_BALA_MAP: return 0.0
    strong_house = DIG_BALA_MAP[planet]
    dist = (house - strong_house) % 12
    if dist > 6: dist = 12 - dist
    return (6 - dist) / 6.0 * 60.0

def calculate_kendra_adi_bala(house: int) -> float:
    if house in [1, 4, 7, 10]: return KENDRA_ADI_SCORES["Kendra"]
    if house in [2, 5, 8, 11]: return KENDRA_ADI_SCORES["Panapara"]
    return KENDRA_ADI_SCORES["Apoklima"]

def calculate_kala_bala(planet: str, is_day: bool) -> float:
    day_planets = {"Sun", "Jupiter", "Venus"}
    night_planets = {"Moon", "Mars", "Saturn"}
    if planet == "Mercury": return 60.0
    if is_day and planet in day_planets: return 60.0
    if not is_day and planet in night_planets: return 60.0
    return 30.0

def get_varga_relationship_score(planet: str, rashi_idx: int, planets_house_map: Dict[str, int]) -> float:
    """Determine relationship with sign lord and return points."""
    lord = RASHI_LORDS[rashi_idx]
    if lord == planet:
        return VargaPoints["Own Sign"]

    # Needs temporal friendship for "Great Friend" etc.
    # We pass the houses for this.
    p_house = planets_house_map.get(planet)
    l_house = planets_house_map.get(lord)

    if p_house is not None and l_house is not None:
        relationship = get_compound_friendship(lord, planet, l_house, p_house)
        return VargaPoints.get(relationship, 10)
    return 10.0

def calculate_shadbala(chart_data: Dict[str, Any], is_day: bool = True) -> Dict[str, Dict[str, float]]:
    """
    Calculate a more complete Shadbala score.
    Returns scores in Virupas.
    """
    results = {}
    planets = chart_data["planets"]

    # Build house map for temporal friendship
    planets_house_map = {name: data["house"] for name, data in planets.items()}

    for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        p_data = planets[p]
        lon = p_data["longitude"]
        house = p_data["house"]

        # 1. Sthana Bala
        sthana = calculate_exaltation_bala(p, lon)
        sthana += calculate_kendra_adi_bala(house)

        # Sapta-varga-ja Bala
        sv_bala = 0.0
        vargas = ["D1", "D2", "D3", "D7", "D9", "D12", "D30"]
        for v_name in vargas:
            if "divisional_charts" in chart_data and v_name in chart_data["divisional_charts"]:
                v_rashi = chart_data["divisional_charts"][v_name][p]
                sv_bala += get_varga_relationship_score(p, v_rashi, planets_house_map)

        sthana += sv_bala

        # 2. Dig Bala
        dig = calculate_dig_bala(p, house)

        # 3. Kala Bala
        kala = calculate_kala_bala(p, is_day)

        # 4. Naisargika Bala
        naisargika = {
            "Sun": 60, "Moon": 51.43, "Venus": 42.86, "Jupiter": 34.29,
            "Mercury": 25.71, "Mars": 17.14, "Saturn": 8.57
        }.get(p, 0.0)

        total = sthana + dig + kala + naisargika

        results[p] = {
            "sthana_bala": round(sthana, 2),
            "dig_bala": round(dig, 2),
            "kala_bala": round(kala, 2),
            "naisargika_bala": round(naisargika, 2),
            "total_shadbala": round(total, 2),
            "total_rupas": round(total / 60.0, 2)
        }

    return results
