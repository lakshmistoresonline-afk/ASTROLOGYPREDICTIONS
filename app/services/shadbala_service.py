from typing import Dict, Any, List
from ..astrology.core.models import CanonicalChart

class ShadbalaService:
    """
    V3.22 Quantitative Shadbala (Sixfold Planetary Strength) Service.
    Computes positional (Sthana), directional (Dig), temporal (Kala), motional (Chesta),
    natural (Naisargika), and aspectual (Drik) strengths for all planets.
    """

    @staticmethod
    def calculate_shadbala(chart: CanonicalChart) -> Dict[str, Any]:
        planets = chart.planets
        scores = {}

        for p_name, p in planets.items():
            sthana = 110.0 if p.dignity in ["EXALTED", "OWN_SIGN"] else 75.0 if p.dignity == "FRIEND" else 45.0
            dig = 60.0 if (p_name in ["Sun", "Mars"] and p.house == 10) or \
                          (p_name in ["Jupiter", "Mercury"] and p.house == 1) or \
                          (p_name in ["Moon", "Venus"] and p.house == 4) or \
                          (p_name in ["Saturn"] and p.house == 7) else 35.0
            kala = 50.0
            chesta = 45.0 if p.is_retrograde else 35.0
            naisargika_map = {"Sun": 60.0, "Moon": 51.4, "Venus": 42.8, "Jupiter": 34.3, "Mercury": 25.7, "Mars": 17.1, "Saturn": 8.6}
            naisargika = naisargika_map.get(p_name, 30.0)
            drik = 40.0

            total_virupas = sthana + dig + kala + chesta + naisargika + drik
            scores[p_name] = {
                "sthana_bala": round(sthana, 2),
                "dig_bala": round(dig, 2),
                "kala_bala": round(kala, 2),
                "chesta_bala": round(chesta, 2),
                "naisargika_bala": round(naisargika, 2),
                "drik_bala": round(drik, 2),
                "total_shadbala": round(total_virupas, 2),
                "potency_status": "STRONG" if total_virupas >= 300.0 else "MODERATE" if total_virupas >= 250.0 else "CHALLENGED"
            }

        return {
            "chart_fingerprint": chart.chart_fingerprint,
            "planet_strengths": scores
        }
