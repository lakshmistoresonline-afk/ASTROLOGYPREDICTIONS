from typing import Dict, Any

# Moorti Nirnaya (Silver, Gold, Copper, Iron)
# Based on where transit Moon is from natal Moon when a planet enters a new sign.
# 1, 6, 11: Swarna (Gold) - Very Favorable
# 2, 5, 9: Rajat (Silver) - Favorable
# 3, 7, 10: Tamra (Copper) - Moderate
# 4, 8, 12: Loha (Iron) - Challenging

MOORTI_TYPES = {
    1: ("Swarna (Gold)", "Highly Auspicious"),
    6: ("Swarna (Gold)", "Highly Auspicious"),
    11: ("Swarna (Gold)", "Highly Auspicious"),
    2: ("Rajat (Silver)", "Auspicious"),
    5: ("Rajat (Silver)", "Auspicious"),
    9: ("Rajat (Silver)", "Auspicious"),
    3: ("Tamra (Copper)", "Neutral/Moderate"),
    7: ("Tamra (Copper)", "Neutral/Moderate"),
    10: ("Tamra (Copper)", "Neutral/Moderate"),
    4: ("Loha (Iron)", "Challenging"),
    8: ("Loha (Iron)", "Challenging"),
    12: ("Loha (Iron)", "Challenging"),
}

def calculate_moorti(natal_moon_rashi: int, transit_moon_rashi: int) -> Dict[str, str]:
    """Calculate the Moorti status for a specific transit moment."""
    # Count from natal Moon to transit Moon
    rel_house = (transit_moon_rashi - natal_moon_rashi + 12) % 12 + 1

    name, quality = MOORTI_TYPES.get(rel_house, ("Loha", "Challenging"))

    return {
        "rel_house": rel_house,
        "moorti_name": name,
        "quality": quality
    }
