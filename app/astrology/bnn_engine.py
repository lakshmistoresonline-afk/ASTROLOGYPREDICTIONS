"""
Bhrigu Nandi Nadi (BNN) Chain & Progression Engine (Module 7 - Part 1).
Calculates directional trines (1, 5, 9), adjacent (2, 12), and 7th opposition linkages,
ranks conjunct planets by exact degree longitude, and computes Jupiter/Saturn/Rahu progressions.
"""
from typing import Dict, Any, List

ELEMENT_GROUPS = {
    0: "FIRE", 1: "EARTH", 2: "AIR", 3: "WATER",
    4: "FIRE", 5: "EARTH", 6: "AIR", 7: "WATER",
    8: "FIRE", 9: "EARTH", 10: "AIR", 11: "WATER"
}

class BNNEngine:
    """
    Bhrigu Nandi Nadi (BNN) Planetary Chain & Progression Engine.
    """

    @staticmethod
    def calculate_bnn_linkages(planets: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Calculates directional trines (1-5-9), adjacent (2-12), and 7th opposition linkages.
        """
        linkages = []
        p_names = list(planets.keys())

        for i in range(len(p_names)):
            p1_name = p_names[i]
            p1 = planets[p1_name]
            p1_lon = getattr(p1, "longitude", p1 if isinstance(p1, (int, float)) else 0.0)
            p1_rashi = int(p1_lon // 30)
            p1_element = ELEMENT_GROUPS.get(p1_rashi, "FIRE")

            for j in range(i + 1, len(p_names)):
                p2_name = p_names[j]
                p2 = planets[p2_name]
                p2_lon = getattr(p2, "longitude", p2 if isinstance(p2, (int, float)) else 0.0)
                p2_rashi = int(p2_lon // 30)
                p2_element = ELEMENT_GROUPS.get(p2_rashi, "FIRE")

                # Directional Trine (1st, 5th, 9th - Same Element)
                if p1_element == p2_element:
                    linkages.append({
                        "p1": p1_name, "p2": p2_name, "type": "DIRECTIONAL_TRINE_1_5_9", "element": p1_element
                    })

                # Adjacent Signs (2nd, 12th)
                r_diff = abs(p1_rashi - p2_rashi) % 12
                if r_diff in [1, 11]:
                    linkages.append({
                        "p1": p1_name, "p2": p2_name, "type": "ADJACENT_LINKAGE_2_12"
                    })

                # Opposition (7th Sign)
                if r_diff == 6:
                    linkages.append({
                        "p1": p1_name, "p2": p2_name, "type": "OPPOSITION_7TH"
                    })

        return linkages

    @staticmethod
    def calculate_bnn_progressions(age: int) -> Dict[str, Any]:
        """
        Calculates BNN progressions:
        - Jupiter: 12 years per sign
        - Saturn: 30 years per sign
        - Rahu / Ketu: 1.5 years per sign
        """
        jup_sign_shift = int(age // 12) % 12
        sat_sign_shift = int(age // 30) % 12
        rahu_sign_shift = int(age // 1.5) % 12

        return {
            "age": age,
            "jupiter_progression_sign_shift": jup_sign_shift,
            "saturn_progression_sign_shift": sat_sign_shift,
            "rahu_progression_sign_shift": rahu_sign_shift
        }

bnn_engine = BNNEngine()
