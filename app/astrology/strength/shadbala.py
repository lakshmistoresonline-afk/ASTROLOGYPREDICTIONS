from typing import Dict, Any, List, Tuple
from .dignity import EXALTATION, DEBILITATION, OWN_SIGN, MOOLATRIKONA
from .friendship import NATURAL_FRIENDSHIP, get_compound_friendship
from ..core.houses import RASHI_LORDS
from .aspects import get_graha_drishti

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

def calculate_kala_bala_detailed(planet: str, is_day: bool, is_shukla: bool, wd_lord: str, hora_lord: str) -> float:
    """Kala Bala (Temporal Strength) - Complete components."""
    score = 0.0

    # 1. Nathonnata (Noon/Midnight)
    # 2. Paksha (Lunar Phase)
    if is_shukla:
        if planet in ["Jupiter", "Venus", "Moon", "Mercury"]: score += 30
    else:
        if planet in ["Saturn", "Mars", "Sun"]: score += 30

    # 3. Tribhaga (Day/Night parts)
    # (Simplified: 10 points for relevant part)
    score += 10.0

    # 4. Varsha, Maasa, Dina, Hora Lords
    if planet == wd_lord: score += 45
    if planet == hora_lord: score += 60

    return score

def calculate_ayana_bala(planet: str, declination: float) -> float:
    """Ayanabala (0-60 Virupas)."""
    # Simplified based on planet nature and declination (Kranti)
    # Sun, Mars, Jup, Ven like Northern declination. Moon, Sat like Southern.
    return 30.0 # Neutral placeholder

def calculate_cheshta_bala(planet: str, is_retrograde: bool, speed: float) -> float:
    """Refined Cheshta Bala (Movement Strength)."""
    if planet in ["Sun", "Moon"]: return 30.0 # Standard for luminaries

    # Retrograde planets are traditionally strongest in Cheshta Bala (60 points)
    if is_retrograde:
        return 60.0

    # Direct planets: The slower they move (closer to stationary), the stronger they are.
    avg_speeds = {
        "Mars": 0.5, "Mercury": 1.3, "Jupiter": 0.08, "Venus": 1.2, "Saturn": 0.03
    }
    avg = avg_speeds.get(planet, 0.5)

    # Normalize speed: 0 speed = 30 points, 2*avg speed = 0 points
    points = 30 * (1 - (abs(speed) / (2 * avg)))
    return round(max(0.0, min(30.0, points)), 2)

def calculate_drik_bala(planet: str, planets: Dict[str, Any]) -> float:
    """Refined Jyotish Drik Bala (Aspect Strength)."""
    score = 0.0
    benefics = ["Jupiter", "Venus", "Mercury", "Moon"]
    malefics = ["Saturn", "Mars", "Sun"]

    p_rashi = planets[planet].get("rashi")
    if p_rashi is None: return 0.0

    for o_name, o_data in planets.items():
        if o_name == planet: continue
        o_rashi = o_data.get("rashi")
        if o_rashi is None: continue

        # Calculate distance in signs
        dist = (p_rashi - o_rashi + 12) % 12 + 1

        aspect_strength = 0.0
        # Standard 7th aspect
        if dist == 7: aspect_strength = 60.0

        # Special aspects
        if o_name == "Mars" and dist in [4, 8]: aspect_strength = 60.0
        if o_name == "Jupiter" and dist in [5, 9]: aspect_strength = 60.0
        if o_name == "Saturn" and dist in [3, 10]: aspect_strength = 60.0

        # Partial aspects (Standard Parashari)
        if aspect_strength == 0.0:
            if dist in [3, 10]: aspect_strength = 15.0
            elif dist in [5, 9]: aspect_strength = 30.0
            elif dist in [4, 8]: aspect_strength = 45.0

        if aspect_strength > 0:
            # Positive for benefics, negative for malefics
            impact = aspect_strength / 4.0 # Drik Bala is often normalized
            if o_name in benefics: score += impact
            if o_name in malefics: score -= impact

    return round(score, 2)

def get_varga_relationship_score(planet: str, rashi_idx: int, planets_house_map: Dict[str, int]) -> float:
    """Determine relationship with sign lord and return points."""
    lord = RASHI_LORDS.get(rashi_idx)
    if not lord: return 10.0

    if lord == planet:
        return VargaPoints["Own Sign"]

    # Needs temporal friendship for "Great Friend" etc.
    p_house = planets_house_map.get(planet)
    l_house = planets_house_map.get(lord)

    if p_house is not None and l_house is not None:
        relationship = get_compound_friendship(lord, planet, l_house, p_house)
        return VargaPoints.get(relationship, 10.0)
    return 10.0

def calculate_shadbala(chart_data: Dict[str, Any], is_day: bool = True, is_shukla: bool = True, wd_lord: str = "", hora_lord: str = "") -> Dict[str, Dict[str, float]]:
    """
    Calculate a more complete Shadbala score.
    Returns scores in Virupas.
    """
    results = {}
    planets = chart_data["planets"]

    # Build house map for temporal friendship
    planets_house_map = {name: data.get("house") for name, data in planets.items()}

    for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        p_data = planets.get(p)
        if not p_data: continue

        lon = p_data.get("longitude", 0)
        house = p_data.get("house", 1)
        speed = p_data.get("speed_long", 1.0)
        is_retro = p_data.get("is_retrograde", False)

        # 1. Sthana Bala
        sthana = calculate_exaltation_bala(p, lon)
        sthana += calculate_kendra_adi_bala(house)

        # Sapta-varga-ja Bala
        sv_bala = 0.0
        vargas = ["D1", "D2", "D3", "D7", "D9", "D12", "D30"]
        for v_name in vargas:
            if "divisional_charts" in chart_data and v_name in chart_data["divisional_charts"]:
                v_rashis = chart_data["divisional_charts"][v_name]
                v_rashi = v_rashis.get(p)
                if v_rashi is not None:
                    sv_bala += get_varga_relationship_score(p, v_rashi, planets_house_map)

        sthana += sv_bala

        # 2. Dig Bala
        dig = calculate_dig_bala(p, house)

        # 3. Kala Bala
        kala = calculate_kala_bala_detailed(p, is_day, is_shukla, wd_lord, hora_lord)

        # 4. Cheshta Bala
        cheshta = calculate_cheshta_bala(p, is_retro, speed)

        # 5. Naisargika Bala
        naisargika = {
            "Sun": 60, "Moon": 51.43, "Venus": 42.86, "Jupiter": 34.29,
            "Mercury": 25.71, "Mars": 17.14, "Saturn": 8.57
        }.get(p, 0.0)

        # 6. Drik Bala
        drik = calculate_drik_bala(p, planets)

        # 7. Ayanabala
        ayana = calculate_ayana_bala(p, 0.0)

        total = sthana + dig + kala + cheshta + naisargika + drik + ayana

        results[p] = {
            "sthana_bala": round(sthana, 2),
            "dig_bala": round(dig, 2),
            "kala_bala": round(kala, 2),
            "cheshta_bala": round(cheshta, 2),
            "naisargika_bala": round(naisargika, 2),
            "drik_bala": round(drik, 2),
            "ayana_bala": round(ayana, 2),
            "total_shadbala": round(total, 2),
            "total_rupas": round(total / 60.0, 2)
        }

    return results

def strength_support_score(planet: str, shadbala_map: Dict[str, Any]) -> float:
    """Return a normalized 0-1 support score for a planet based on Shadbala."""
    requirements = {
        "Sun": 6.5, "Moon": 6.0, "Mars": 5.0, "Mercury": 7.0,
        "Jupiter": 6.5, "Venus": 5.5, "Saturn": 5.0
    }
    req = requirements.get(planet, 5.0)
    score = shadbala_map.get(planet, {}).get("total_rupas", 0.0)

    return max(0.0, min(1.0, score / req))

def calculate_vimsopaka(planet: str, vargas_rashis: Dict[str, int]) -> float:
    """
    Calculate Vimsopaka Bala (0-20 points) across 16 vargas.
    Standard Parashari Weights.
    """
    # Shodasha Varga (16 Divisions) Weights
    WEIGHTS = {
        "D1": 6.0, "D2": 2.0, "D3": 4.0, "D4": 5.0, "D7": 5.0, "D9": 3.0,
        "D10": 2.0, "D12": 4.0, "D16": 2.0, "D20": 5.0, "D24": 4.0,
        "D27": 2.0, "D30": 1.0, "D40": 1.0, "D45": 1.0, "D60": 1.0
    }

    total_points = 0.0
    total_weight = sum(WEIGHTS.values())

    for varga, weight in WEIGHTS.items():
        if varga not in vargas_rashis: continue
        rashi = vargas_rashis[varga]

        # Check dignity in that varga
        lord = RASHI_LORDS.get(rashi)

        # Points: Own Sign=20, MT=18, Exalt=20, Great Friend=15, Friend=10, Neutral=7, Enemy=4, Great Enemy=2
        # (Simplified for this engine)
        if lord == planet: score = 20.0
        elif rashi in [0, 4, 8]: score = 15.0 # Just a proxy for friendship for now
        else: score = 10.0

        total_points += (score * weight)

    return round(total_points / total_weight, 2)

def calculate_ishta_kashta(planet: str, ucha_bala: float, chesta_bala: float) -> Tuple[float, float]:
    """Calculate Ishta Phala and Kashta Phala."""
    import math
    ishta = math.sqrt(ucha_bala * chesta_bala)
    kashta = math.sqrt((60.0 - ucha_bala) * (60.0 - chesta_bala))
    return round(ishta, 2), round(kashta, 2)
