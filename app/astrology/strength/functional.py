from typing import Dict, List, Set

# Houses and their natures
KENDRA = {1, 4, 7, 10}
TRIKONA = {1, 5, 9}
DUSTHANA = {6, 8, 12}
TRISHADAYA = {3, 6, 11}
UPACHAYA = {3, 6, 10, 11}

# Rashi Lords
RASHI_LORDS = {
    0: "Mars", 1: "Venus", 2: "Mercury", 3: "Moon",
    4: "Sun", 5: "Mercury", 6: "Venus", 7: "Mars",
    8: "Jupiter", 9: "Saturn", 10: "Saturn", 11: "Jupiter",
}

def get_functional_status(asc_rashi_idx: int) -> Dict[str, str]:
    """
    Determine functional benefic/malefic status for all planets based on Ascendant.
    Simplified version of Parasari rules.
    """
    status = {}
    planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]

    # Map house numbers to rashi indices for this ascendant
    house_to_rashi = {h: (asc_rashi_idx + h - 1) % 12 for h in range(1, 13)}
    rashi_to_house = {v: k for k, v in house_to_rashi.items()}

    planet_to_houses = {p: [] for p in planets}
    for r, l in RASHI_LORDS.items():
        planet_to_houses[l].append(rashi_to_house[r])

    for p in planets:
        houses = planet_to_houses[p]
        is_benefic = False
        is_malefic = False

        # Ruler of 1, 5, 9 is always benefic (unless also ruler of severe malefic house)
        if any(h in TRIKONA for h in houses):
            is_benefic = True

        # Ruler of 3, 6, 11 is malefic
        if any(h in TRISHADAYA for h in houses):
            is_malefic = True

        # Yogakaraka: ruler of both Kendra and Trikona
        has_kendra = any(h in KENDRA for h in houses)
        has_trikona = any(h in TRIKONA for h in houses)

        if has_kendra and has_trikona:
            status[p] = "Yogakaraka"
            continue

        if is_benefic and not is_malefic:
            status[p] = "Functional Benefic"
        elif is_malefic and not is_benefic:
            status[p] = "Functional Malefic"
        elif is_benefic and is_malefic:
            # Mixed, but usually Trikona lordship prevails
            status[p] = "Functional Benefic (Mixed)"
        else:
            status[p] = "Functional Neutral"

    # Rahu/Ketu usually take the nature of their dispositor and planets they conjoin
    status["Rahu"] = "Shadow (Mixed)"
    status["Ketu"] = "Shadow (Mixed)"

    return status
