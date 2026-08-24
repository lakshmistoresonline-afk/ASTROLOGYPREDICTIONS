from typing import Dict, List, Any

# Representative list of 150 Nadi Amshas
NADI_AMSHA_NAMES = [
    "Vasudha", "Vaishnavi", "Brahmi", "Kalakuta", "Yojanai", "Kamala", "Santha", "Vimala", "Vibhuthi", "Vishwaroopa",
    "Pramada", "Varuna", "Kunti", "Kaala", "Bala", "Maya", "Gaya", "Mansa", "Nala", "Loka",
    "Kshema", "Dharani", "Shakti", "Durga", "Kala", "Bala", "Subha", "Shiva", "Priya", "Kama"
]

def get_nadi_amsha(rashi: int, degree: float) -> Dict[str, str]:
    """
    Project the degree into 150 divisions of 12 minutes each.
    Represents high-resolution karmic destiny.
    """
    # Each amsha is 12 minutes (0.2 degrees)
    idx = int(degree / 0.2)
    if idx > 149: idx = 149

    is_fixed = rashi in [1, 4, 7, 10]
    if is_fixed:
        idx = 149 - idx

    name = NADI_AMSHA_NAMES[idx % len(NADI_AMSHA_NAMES)]

    return {
        "name": name,
        "index": idx + 1,
        "interpretation": f"Nadi Amsha {name} suggests a specific karmic 'seed' related to its mythic namesake."
    }
