from typing import Dict, Any

def calculate_mahabote(year: int, weekday: int) -> Dict[str, Any]:
    """
    Burmese Mahabote (Little Key) system.
    Based on Year % 7 and Weekday.
    """
    remainder = (year - 638) % 7 # Burmese Era starts in 638 AD

    # 7 Houses in the Chart:
    # 1. Atula (Exalted)
    # 2. Raja (King)
    # 3. Thike (Wealth)
    # 4. Bin (Destruction)
    # 5. Marana (Death)
    # 6. Ahtun (Fame)
    # 7. Puti (Rotten)

    # Grid placement depends on the remainder
    # This is a simplified version of the Burmese cycle
    HOUSES = ["Puti", "Bin", "Ahtun", "Thike", "Raja", "Marana", "Atula"]

    # Weekday mapping (Burmese: 0=Sun, 1=Mon, 2=Tue, 3=Wed AM, 4=Thu, 5=Fri, 6=Sat, 7=Wed PM)
    PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]

    # The house a planet falls in determines its "Mahabote" quality
    # Simplified: Find which house the birth planet (weekday lord) falls in
    house_idx = (weekday - remainder + 7) % 7

    return {
        "birth_weekday_lord": PLANETS[weekday % 7],
        "mahabote_house": HOUSES[house_idx],
        "interpretation": f"In the Burmese Mahabote system, your birth planet {PLANETS[weekday % 7]} falls in the house of {HOUSES[house_idx]}."
    }
