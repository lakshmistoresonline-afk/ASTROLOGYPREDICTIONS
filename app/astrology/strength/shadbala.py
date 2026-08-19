from typing import Dict, Any, List
from ..core.planets import PLANETS
from ..core.houses import get_house_from_longitude
from .dignity import EXALTATION, DEBILITATION

# Dig Bala (Directional Strength)
# Sun/Mars: 10th (South), Jupiter/Mercury: 1st (East), Moon/Venus: 4th (North), Saturn: 7th (West)
DIG_BALA_MAP = {
    "Sun": 10, "Mars": 10,
    "Jupiter": 1, "Mercury": 1,
    "Moon": 4, "Venus": 4,
    "Saturn": 7
}

# Kendra-adi Bala (Angle, Succedent, Cadent)
KENDRA_ADI_SCORES = {
    "Kendra": 60,   # 1, 4, 7, 10
    "Panapara": 30, # 2, 5, 8, 11
    "Apoklima": 15  # 3, 6, 9, 12
}

def calculate_exaltation_bala(planet: str, longitude: float) -> float:
    """Calculate Exaltation Bala (0-60 Virupas)."""
    if planet not in EXALTATION:
        return 0.0

    ex_rashi, ex_deg = EXALTATION[planet]
    ex_lon = ex_rashi * 30 + ex_deg

    db_rashi, db_deg = DEBILITATION[planet]
    db_lon = db_rashi * 30 + db_deg

    # Difference from debilitation point
    diff = (longitude - db_lon) % 360
    if diff > 180:
        diff = 360 - diff

    # Max is 180 deg away from debilitation (at exaltation point)
    # 180 degrees = 60 virupas
    return (diff / 180.0) * 60.0

def calculate_dig_bala(planet: str, house: int) -> float:
    """Calculate Dig Bala (0-60 Virupas)."""
    if planet not in DIG_BALA_MAP:
        return 0.0

    strong_house = DIG_BALA_MAP[planet]
    # Simplistic version: Max in strong house, Min in opposite
    # Full version requires exact longitude of house cusps.
    # Here we use house number approximation.
    dist = (house - strong_house) % 12
    if dist > 6:
        dist = 12 - dist

    # 0 distance = 60, 6 distance = 0
    return (6 - dist) / 6.0 * 60.0

def calculate_kendra_adi_bala(house: int) -> float:
    if house in [1, 4, 7, 10]: return KENDRA_ADI_SCORES["Kendra"]
    if house in [2, 5, 8, 11]: return KENDRA_ADI_SCORES["Panapara"]
    return KENDRA_ADI_SCORES["Apoklima"]

def calculate_shadbala(chart: Dict[str, Any]) -> Dict[str, Dict[str, float]]:
    """
    Calculate a simplified Shadbala score for all 7 planets.
    Returns scores in Virupas (60 Virupas = 1 Rupa).
    """
    results = {}
    planets = chart["planets"]

    for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        p_data = planets[p]
        lon = p_data["longitude"]
        house = p_data["house"]

        # 1. Sthana Bala (Partial)
        sthana = calculate_exaltation_bala(p, lon)
        sthana += calculate_kendra_adi_bala(house)
        # TODO: Add Sapta-varga-ja Bala

        # 2. Dig Bala
        dig = calculate_dig_bala(p, house)

        # 3. Naisargika Bala (Natural Strength)
        # Sun=60, Moon=51.43, Venus=42.86, Jup=34.29, Merc=25.71, Mars=17.14, Sat=8.57
        naisargika = {
            "Sun": 60, "Moon": 51.43, "Venus": 42.86, "Jupiter": 34.29,
            "Mercury": 25.71, "Mars": 17.14, "Saturn": 8.57
        }.get(p, 0.0)

        total = sthana + dig + naisargika
        # TODO: Add Kala Bala, Cheshta Bala, Drik Bala

        results[p] = {
            "sthana_bala": round(sthana, 2),
            "dig_bala": round(dig, 2),
            "naisargika_bala": round(naisargika, 2),
            "total_shadbala": round(total, 2),
            "total_rupas": round(total / 60.0, 2)
        }

    return results
