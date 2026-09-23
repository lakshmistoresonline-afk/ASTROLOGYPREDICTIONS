"""
Jaimini Chara Dasha & Karaka Interlocking Engine (Module 8 - Task 8.1).
Ranks planets by degree within signs to derive 7 Chara Karakas (AK, AmK, BK, MK, PK, GK, DK)
and evaluates Jaimini sign aspect activations.
"""
from typing import Dict, Any, List

KARAKA_ROLES = ["Atmakaraka", "Amatyakaraka", "Bhratrukaraka", "Matrukaraka", "Putrakaraka", "Gnatikaraka", "Darakaraka"]

class JaiminiEngine:
    """
    Computes 7 Chara Karakas and evaluates Jaimini Chara Dasha sign activations.
    """

    @staticmethod
    def calculate_chara_karakas(planets: Dict[str, Any]) -> Dict[str, str]:
        """
        Ranks 7 classical planets (Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn)
        by longitude degree within their respective sign (0-30 deg).
        """
        ranked = []
        for name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
            p = planets.get(name)
            if not p: continue
            deg = getattr(p, "degree", p.longitude % 30.0 if hasattr(p, "longitude") else 0.0)
            ranked.append((deg, name))

        # Sort descending by degree in sign
        ranked.sort(key=lambda x: x[0], reverse=True)

        karakas = {}
        for idx, (deg, p_name) in enumerate(ranked[:7]):
            karakas[KARAKA_ROLES[idx]] = p_name

        return karakas

    @staticmethod
    def evaluate_jaimini_activation(
        domain: str,
        chara_karakas: Dict[str, str],
        active_chara_sign: int,
        planets: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Cross-verifies if active Jaimini Chara Dasha sign contains or aspects key Karakas.
        - Career: Amatyakaraka (AmK)
        - Self/Identity: Atmakaraka (AK)
        - Relationships: Darakaraka (DK)
        """
        target_karaka_map = {
            "Career": "Amatyakaraka",
            "Career & Authority": "Amatyakaraka",
            "Finance": "Amatyakaraka",
            "Personality": "Atmakaraka",
            "Marriage": "Darakaraka",
            "Marriage & Relationships": "Darakaraka"
        }

        req_karaka_role = target_karaka_map.get(domain, "Atmakaraka")
        target_planet = chara_karakas.get(req_karaka_role)

        is_activated = False
        if target_planet and target_planet in planets:
            p_obj = planets[target_planet]
            p_rashi = getattr(p_obj, "rashi", int(p_obj.longitude // 30) if hasattr(p_obj, "longitude") else 0)

            # Check if active Jaimini sign equals planet rashi or forms Jaimini sign aspect
            if active_chara_sign == p_rashi or (active_chara_sign - p_rashi) % 3 == 0:
                is_activated = True

        return {
            "domain": domain,
            "target_karaka_role": req_karaka_role,
            "target_planet": target_planet,
            "active_chara_sign": active_chara_sign,
            "jaimini_activated": is_activated,
            "confluence_boost": 0.25 if is_activated else 0.0
        }

jaimini_engine = JaiminiEngine()
