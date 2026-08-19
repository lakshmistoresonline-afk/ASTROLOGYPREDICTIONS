from typing import Dict, Any

# Exaltation and Debilitation points
# Format: (Rashi index, degree)
EXALTATION = {
    "Sun": (0, 10), "Moon": (1, 3), "Mars": (9, 28),
    "Mercury": (5, 15), "Jupiter": (3, 5), "Venus": (11, 27),
    "Saturn": (6, 20), "Rahu": (1, 20), "Ketu": (7, 20),
}

DEBILITATION = {
    "Sun": (6, 10), "Moon": (7, 3), "Mars": (3, 28),
    "Mercury": (11, 15), "Jupiter": (9, 5), "Venus": (5, 27),
    "Saturn": (0, 20), "Rahu": (7, 20), "Ketu": (1, 20),
}

OWN_SIGN = {
    "Sun": [4], "Moon": [3], "Mars": [0, 7], "Mercury": [2, 5],
    "Jupiter": [8, 11], "Venus": [1, 6], "Saturn": [9, 10],
}

MOOLATRIKONA = {
    "Sun": (4, 0, 20),      # Simha 0-20
    "Moon": (1, 3, 30),     # Vrishabha 3-30
    "Mars": (0, 0, 12),     # Mesha 0-12
    "Mercury": (5, 16, 20), # Kanya 16-20
    "Jupiter": (8, 0, 10),  # Dhanu 0-10
    "Venus": (6, 0, 15),    # Tula 0-15
    "Saturn": (10, 0, 20),  # Kumbha 0-20
}

def get_dignity(planet: str, rashi_idx: int, degree: float) -> str:
    """Return the dignity of a planet."""
    if planet in EXALTATION:
        ex_rashi, ex_deg = EXALTATION[planet]
        if rashi_idx == ex_rashi:
            # Strictly speaking, exaltation is a point, but many use the whole sign
            # Deep exaltation is exactly at that point.
            if abs(degree - ex_deg) < 1.0:
                return "Exalted (Deep)"
            return "Exalted"

    if planet in DEBILITATION:
        db_rashi, db_deg = DEBILITATION[planet]
        if rashi_idx == db_rashi:
            if abs(degree - db_deg) < 1.0:
                return "Debilitated (Deep)"
            return "Debilitated"

    if planet in MOOLATRIKONA:
        mt_rashi, mt_start, mt_end = MOOLATRIKONA[planet]
        if rashi_idx == mt_rashi and mt_start <= degree <= mt_end:
            return "Moolatrikona"

    if planet in OWN_SIGN:
        if rashi_idx in OWN_SIGN[planet]:
            return "Own Sign"

    return "Neutral"
