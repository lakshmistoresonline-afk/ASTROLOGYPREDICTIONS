from typing import Dict, List, Any
from .houses import RASHI_LORDS

def calculate_harsha_bala(planets: Dict[str, Any], asc_rashi: int) -> Dict[str, int]:
    """
    Harsha Bala (Happiness Strength) for Tajika/Varshaphala.
    Four components: Sthana (House), Rashi (Exaltation/Sign), Uccha (Position), and Strength.
    """
    # Standard Harsha Bala points for 7 planets
    results = {}

    # Position mapping for Harsha Bala
    HB_POSITIONS = {
        "Sun": 9, "Moon": 3, "Mars": 6, "Mercury": 1,
        "Jupiter": 11, "Venus": 5, "Saturn": 12
    }

    for name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        p = planets[name]
        score = 0

        # 1. First Strength (Placement in strong house)
        if p.house == HB_POSITIONS[name]:
            score += 5

        # 2. Second Strength (Own sign or Exaltation)
        if "Exalted" in p.dignity or p.dignity == "Own Sign":
            score += 5

        # 3. Third Strength (Feminine/Masculine signs based on nature)
        # Masculine (Sun, Mars, Jup), Feminine (Moon, Ven, Sat), Neutral (Merc)
        is_odd = p.rashi % 2 == 0 # 0=Aries (Masculine)
        if name in ["Sun", "Mars", "Jupiter"] and is_odd: score += 5
        if name in ["Moon", "Venus", "Saturn"] and not is_odd: score += 5
        if name == "Mercury": score += 5 # Merc is always happy in this component

        # 4. Fourth Strength (Day/Night birth happiness)
        # (Assuming is_day context would be passed, for now use natal context or simplified)

        results[name] = score

    return results

def calculate_panchavargiya_bala(planets: Dict[str, Any]) -> Dict[str, float]:
    """
    Panchavargiya Bala (5-fold strength):
    Kshetra (Sign), Hora, Drekkana, Navamsha, Dwadashamsha.
    """
    results = {}

    for name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        p = planets[name]
        total = 0.0

        # kshetra (Sign)
        if "Exalted" in p.dignity: total += 30
        elif p.dignity == "Own Sign": total += 22.5
        elif "Friend" in p.dignity: total += 15
        else: total += 7.5

        # (Simplified Drekkana/Navamsha components based on D1 dignity proxy)
        total += 15.0 # Average for other 4 components

        results[name] = total

    return results
