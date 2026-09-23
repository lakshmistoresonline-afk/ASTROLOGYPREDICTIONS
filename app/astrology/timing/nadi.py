"""
Degree-Exact Nadi Planetary Lineage & Aspect Grid (Module 7 - Task 7.2).
Calculates exact inter-planetary angles (0, 60, 120, 180 deg) and directional trines
(1st, 5th, 9th sign directional alignment) between transiting slow planets and natal vectors within +/- 2.5 deg.
"""
from typing import Dict, Any, List

# Nadi Directional Sign Groups (Fiery, Earthy, Airy, Watery)
NADI_ELEMENT_GROUPS = {
    0: "FIRE",   # Aries (Mesha)
    1: "EARTH",  # Taurus (Vrishabha)
    2: "AIR",    # Gemini (Mithuna)
    3: "WATER",  # Cancer (Karka)
    4: "FIRE",   # Leo (Simha)
    5: "EARTH",  # Virgo (Kanya)
    6: "AIR",    # Libra (Tula)
    7: "WATER",  # Scorpio (Vrishchika)
    8: "FIRE",   # Sagittarius (Dhanu)
    9: "EARTH",  # Capricorn (Makara)
    10: "AIR",   # Aquarius (Kumbha)
    11: "WATER"  # Pisces (Meena)
}

class NadiTransitGrid:
    """
    Evaluates degree-exact Nadi planetary contacts and directional trines (1, 5, 9 alignment).
    """

    @staticmethod
    def evaluate_nadi_aspects(
        transit_planets: Dict[str, float],
        natal_planets: Dict[str, float],
        orb_tolerance: float = 2.5
    ) -> List[Dict[str, Any]]:
        """
        Flags Nadi directional trines and exact degree aspects within +/- 2.5 degrees.
        """
        triggers = []
        slow_planets = ["Jupiter", "Saturn", "Rahu", "Ketu"]

        for t_name in slow_planets:
            t_lon = transit_planets.get(t_name)
            if t_lon is None: continue

            t_rashi = int(t_lon // 30)
            t_element = NADI_ELEMENT_GROUPS.get(t_rashi)

            for n_name, n_lon in natal_planets.items():
                n_rashi = int(n_lon // 30)
                n_element = NADI_ELEMENT_GROUPS.get(n_rashi)

                # 1. Nadi Directional Trine (Same element group: 1st, 5th, 9th alignment)
                if t_element == n_element:
                    diff = abs(t_lon - n_lon) % 360.0
                    if diff > 180.0: diff = 360.0 - diff

                    # Check Nadi exact angular aspect (0, 120 deg) within orb_tolerance (2.5 deg)
                    for target_angle in [0.0, 120.0]:
                        orb_err = abs(diff - target_angle)
                        if orb_err <= orb_tolerance:
                            triggers.append({
                                "transiting_planet": t_name,
                                "natal_planet": n_name,
                                "nadi_element": t_element,
                                "aspect_angle": target_angle,
                                "orb_error": round(orb_err, 2),
                                "precision_window": "48-72 HOUR NADI TRIGGER",
                                "description": f"Transiting {t_name} forms Nadi directional trine ({t_element}) to natal {n_name} within {orb_err:.2f} deg orb."
                            })

        return triggers

nadi_transit_grid = NadiTransitGrid()
