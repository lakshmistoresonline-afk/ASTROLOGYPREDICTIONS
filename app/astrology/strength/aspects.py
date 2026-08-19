from typing import List

def get_graha_drishti(planet: str, rashi_idx: int) -> List[int]:
    """Return a list of Rashi indices that the planet aspects."""
    # All planets aspect the 7th sign from their position
    aspects = [(rashi_idx + 6) % 12]

    # Special aspects
    if planet == "Mars":
        aspects.append((rashi_idx + 3) % 12) # 4th
        aspects.append((rashi_idx + 7) % 12) # 8th
    elif planet == "Jupiter":
        aspects.append((rashi_idx + 4) % 12) # 5th
        aspects.append((rashi_idx + 8) % 12) # 9th
    elif planet == "Saturn":
        aspects.append((rashi_idx + 2) % 12) # 3rd
        aspects.append((rashi_idx + 9) % 12) # 10th
    elif planet in ["Rahu", "Ketu"]:
        # Rahu/Ketu aspects are debatable, but 5/9 are commonly used
        aspects.append((rashi_idx + 4) % 12)
        aspects.append((rashi_idx + 8) % 12)

    return list(set(aspects))

def is_aspected_by(target_rashi: int, aspecting_planet: str, aspecting_planet_rashi: int) -> bool:
    """Check if a target rashi is aspected by a specific planet."""
    drishtis = get_graha_drishti(aspecting_planet, aspecting_planet_rashi)
    return target_rashi in drishtis
