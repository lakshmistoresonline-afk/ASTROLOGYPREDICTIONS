from typing import Dict, List, Any

# Bindu contribution tables (Relative house from planet/Lagna)
BINDU_TABLES = {
    "Sun": {
        "Sun": [1, 2, 4, 7, 8, 9, 10, 11],
        "Moon": [3, 6, 10, 11],
        "Mars": [1, 2, 4, 7, 8, 9, 10, 11],
        "Mercury": [3, 5, 6, 9, 10, 11, 12],
        "Jupiter": [5, 6, 9, 11],
        "Venus": [6, 7, 12],
        "Saturn": [1, 2, 4, 7, 8, 9, 10, 11],
        "Lagna": [3, 4, 6, 10, 11, 12],
    },
    "Moon": {
        "Sun": [3, 6, 7, 8, 10, 11],
        "Moon": [1, 3, 6, 7, 10, 11],
        "Mars": [2, 3, 5, 6, 9, 10, 11],
        "Mercury": [1, 3, 4, 5, 7, 8, 10, 11],
        "Jupiter": [1, 4, 7, 8, 10, 11, 12],
        "Venus": [3, 4, 5, 7, 9, 10, 11],
        "Saturn": [3, 5, 6, 11],
        "Lagna": [3, 6, 10, 11],
    },
    "Mars": {
        "Sun": [3, 5, 6, 10, 11],
        "Moon": [3, 6, 11],
        "Mars": [1, 2, 4, 7, 8, 10, 11],
        "Mercury": [3, 5, 6, 11],
        "Jupiter": [6, 10, 11, 12],
        "Venus": [6, 8, 11, 12],
        "Saturn": [1, 4, 7, 8, 9, 10, 11],
        "Lagna": [1, 3, 6, 10, 11],
    },
    "Mercury": {
        "Sun": [5, 6, 9, 11, 12],
        "Moon": [2, 4, 6, 8, 10, 11],
        "Mars": [1, 2, 4, 7, 8, 9, 10, 11],
        "Mercury": [1, 3, 5, 6, 9, 10, 11, 12],
        "Jupiter": [6, 8, 11, 12],
        "Venus": [1, 2, 3, 4, 5, 8, 9, 11],
        "Saturn": [1, 2, 4, 7, 8, 9, 10, 11],
        "Lagna": [1, 2, 4, 6, 8, 10, 11],
    },
    "Jupiter": {
        "Sun": [1, 2, 3, 4, 7, 8, 9, 10, 11],
        "Moon": [2, 5, 7, 9, 11],
        "Mars": [1, 2, 4, 7, 8, 10, 11],
        "Mercury": [1, 2, 4, 5, 6, 9, 10, 11],
        "Jupiter": [1, 2, 3, 4, 7, 8, 10, 11],
        "Venus": [2, 5, 6, 9, 10, 11],
        "Saturn": [3, 5, 6, 12],
        "Lagna": [1, 2, 4, 5, 6, 7, 9, 10, 11],
    },
    "Venus": {
        "Sun": [8, 11, 12],
        "Moon": [1, 2, 3, 4, 5, 8, 9, 11, 12],
        "Mars": [3, 5, 6, 9, 11, 12],
        "Mercury": [3, 5, 6, 9, 11],
        "Jupiter": [5, 8, 9, 10, 11],
        "Venus": [1, 2, 3, 4, 5, 8, 9, 10, 11],
        "Saturn": [3, 4, 5, 8, 9, 10, 11],
        "Lagna": [1, 2, 3, 4, 5, 8, 9, 11],
    },
    "Saturn": {
        "Sun": [1, 2, 4, 7, 8, 10, 11],
        "Moon": [3, 6, 11],
        "Mars": [3, 5, 6, 10, 11, 12],
        "Mercury": [6, 8, 9, 10, 11, 12],
        "Jupiter": [5, 6, 11, 12],
        "Venus": [6, 11, 12],
        "Saturn": [3, 5, 6, 11],
        "Lagna": [1, 3, 4, 6, 10, 11],
    }
}

PLANET_MULTIPLIERS = {
    "Sun": 5, "Moon": 5, "Mars": 8, "Mercury": 5,
    "Jupiter": 10, "Venus": 7, "Saturn": 5
}
RASHI_MULTIPLIERS = [7, 10, 8, 4, 10, 5, 7, 8, 9, 5, 11, 12]

def calculate_bav(planet: str, planet_rashis: Dict[str, int]) -> List[int]:
    """Calculate Bhinna Ashtakavarga (BAV) for a planet."""
    if planet not in BINDU_TABLES:
        return [0] * 12
    bav = [0] * 12
    table = BINDU_TABLES[planet]
    for source_planet, houses in table.items():
        source_rashi = planet_rashis.get(source_planet)
        if source_rashi is None: continue
        for house in houses:
            target_rashi = (source_rashi + house - 1) % 12
            bav[target_rashi] += 1
    return bav

def apply_trikona_shodhana(bav: List[int]) -> List[int]:
    """Reduce BAV based on Trikona groups."""
    reduced = list(bav)
    for group in [(0, 4, 8), (1, 5, 9), (2, 6, 10), (3, 7, 11)]:
        vals = [reduced[i] for i in group]
        m = min(vals)
        for i in group:
            reduced[i] -= m
    return reduced

def calculate_shodhya_pinda(bav: List[int], planet_rashis: Dict[str, int], planet_name: str) -> int:
    """Calculate the final Shodhya Pinda for a planet."""
    trikona = apply_trikona_shodhana(bav)
    # Simple Shodhya Pinda calculation (Simplified for performance)
    rashi_sum = sum(trikona[i] * RASHI_MULTIPLIERS[i] for i in range(12))

    # Planet sum: sum of reduced points where planets are located
    planet_sum = 0
    p_rashi = planet_rashis.get(planet_name)
    if p_rashi is not None:
        planet_sum = trikona[p_rashi] * PLANET_MULTIPLIERS.get(planet_name, 5)

    return rashi_sum + planet_sum

def calculate_ashtakavarga(planets_rashi: Dict[str, int], lagna_rashi: int) -> Dict[str, Any]:
    """Calculate BAV, SAV, and Shodhya Pinda."""
    all_rashis = {**planets_rashi, "Lagna": lagna_rashi}
    bav_results = {}
    shodhya_pindas = {}
    sav = [0] * 12

    for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        bav = calculate_bav(p, all_rashis)
        bav_results[p] = bav
        shodhya_pindas[p] = calculate_shodhya_pinda(bav, planets_rashi, p)
        for i in range(12):
            sav[i] += bav[i]

    return {
        "BAV": bav_results,
        "SAV": sav,
        "ShodhyaPinda": shodhya_pindas
    }
