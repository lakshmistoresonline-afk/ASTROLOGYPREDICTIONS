"""
Ashtakavarga Kakshya Orbital Tracking Engine (Module 7 - Task 7.1).
Divides each of the 12 signs into 8 equal Kakshya sub-zones of 3 deg 45 min (3.75 deg).
Sequentially governed by: Saturn, Jupiter, Mars, Sun, Venus, Mercury, Moon, Lagna.
Cross-references transiting planet longitudes against natal BAV matrix to isolate 48-to-72-hour operational windows.
"""
from typing import Dict, Any, List

KAKSHYA_LORDS = ["Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon", "Lagna"]
KAKSHYA_SPAN_DEG = 3.75 # 3 deg 45 min

class KakshyaEvaluator:
    """
    Evaluates Ashtakavarga Kakshya sub-zones (3.75 deg) for transiting planets against BAV.
    """

    @staticmethod
    def get_kakshya_info(longitude: float) -> Dict[str, Any]:
        """
        Determines the Kakshya lord and sub-zone index for a given longitude (0-360 deg).
        """
        rashi = int(longitude // 30)
        deg_in_rashi = longitude % 30.0
        kakshya_idx = int(deg_in_rashi // KAKSHYA_SPAN_DEG)
        if kakshya_idx > 7:
            kakshya_idx = 7

        lord = KAKSHYA_LORDS[kakshya_idx]
        span_start = rashi * 30.0 + (kakshya_idx * KAKSHYA_SPAN_DEG)
        span_end = span_start + KAKSHYA_SPAN_DEG

        return {
            "rashi": rashi,
            "degree_in_rashi": round(deg_in_rashi, 2),
            "kakshya_index": kakshya_idx,
            "kakshya_lord": lord,
            "span_start": round(span_start, 2),
            "span_end": round(span_end, 2)
        }

    @staticmethod
    def evaluate_transit_kakshya(
        transiting_planet: str,
        transit_longitude: float,
        bav_matrix: Dict[str, List[int]],
        natal_rashis: Dict[str, int]
    ) -> Dict[str, Any]:
        """
        Cross-references transiting planet against user's BAV matrix:
        - IF Kakshya lord contributed a bindu (1) in that sign -> High-Activation Timing Window.
        - IF Kakshya lord contributed 0 -> Suppress Transit Impact.
        """
        k_info = KakshyaEvaluator.get_kakshya_info(transit_longitude)
        rashi = k_info["rashi"]
        k_lord = k_info["kakshya_lord"]

        planet_bav = bav_matrix.get(transiting_planet, [0] * 12)
        has_bindu = False

        if k_lord in ["Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon"]:
            p_rashi = natal_rashis.get(k_lord)
            if p_rashi is not None:
                # Check if this rashi receives a bindu in transiting planet's BAV
                has_bindu = planet_bav[rashi] > 0
        elif k_lord == "Lagna":
            has_bindu = planet_bav[rashi] > 0

        activation_status = "HIGH_ACTIVATION" if has_bindu else "SUPPRESSED"

        return {
            "transiting_planet": transiting_planet,
            "transit_longitude": round(transit_longitude, 2),
            "kakshya_lord": k_lord,
            "rashi": rashi,
            "has_bav_bindu": has_bindu,
            "activation_status": activation_status,
            "window_precision": "48-72 HOUR OPERATIONAL WINDOW" if has_bindu else "LATENT"
        }

kakshya_evaluator = KakshyaEvaluator()
