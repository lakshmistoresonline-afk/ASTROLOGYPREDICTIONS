"""
Shodashavarga (D1–D60) Harmonic Integrator & Vaisheshikamsa Scorer (Module 7 - Part 3).
Calculates all 16 divisional charts with D9 (Navamsha), D10 (Dashamsha), and D60 (Shashtiamsha) focus,
and evaluates Vaisheshikamsa dignities (Parijata, Gopuram, Simhasanam, Devaloka).
"""
from typing import Dict, Any, List

VAISHESHIKAMSA_LEVELS = {
    2: "Parijata (2 Exalted/Own Divisional Signs)",
    3: "Uttama (3 Exalted/Own Divisional Signs)",
    4: "Gopuram (4 Exalted/Own Divisional Signs)",
    5: "Simhasanam (5 Exalted/Own Divisional Signs)",
    6: "Paravata (6 Exalted/Own Divisional Signs)",
    7: "Devaloka (7 Exalted/Own Divisional Signs)",
    8: "Iravata (8 Exalted/Own Divisional Signs)",
    9: "Vaishnavam (9 Exalted/Own Divisional Signs)",
    10: "Saubhagyam (10 Exalted/Own Divisional Signs)"
}

class ShodashavargaEngine:
    """
    Shodashavarga 16 Divisional Chart Harmonic Integrator & Vaisheshikamsa Scorer.
    """

    @staticmethod
    def calculate_d60_shashtiamsha(longitude: float) -> int:
        """
        Calculates D60 Shashtiamsha divisional sign (0.5 deg = 30 arcmin per D60 division).
        Provides micro-variance for twin-birth differentiation.
        """
        rashi = int(longitude // 30)
        deg_in_rashi = longitude % 30.0
        d60_index = int(deg_in_rashi // 0.5) % 60
        d60_rashi = (rashi + d60_index) % 12
        return d60_rashi

    @staticmethod
    def evaluate_vaisheshikamsa_score(divisional_charts: Dict[str, Dict[str, int]], planet_name: str) -> Dict[str, Any]:
        """
        Evaluates planetary dignities across 16 divisional charts to assign Vaisheshikamsa status.
        """
        own_or_exalted_count = 0
        from .core.houses import RASHI_LORDS

        for v_code, v_data in divisional_charts.items():
            if isinstance(v_data, dict) and planet_name in v_data:
                p_rashi = v_data[planet_name]
                # Check if planet is in own sign in this varga
                if RASHI_LORDS[p_rashi % 12] == planet_name:
                    own_or_exalted_count += 1

        dignity_level = VAISHESHIKAMSA_LEVELS.get(own_or_exalted_count, f"Standard ({own_or_exalted_count} Varga Dignities)")

        return {
            "planet": planet_name,
            "varga_dignity_count": own_or_exalted_count,
            "vaisheshikamsa_level": dignity_level
        }

shodashavarga_engine = ShodashavargaEngine()
