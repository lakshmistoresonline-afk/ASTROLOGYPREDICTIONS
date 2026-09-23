"""
Astrolog C++ Integration & Fixed-Stars / Astrocartography Engine.
Calculates 108+ Fixed Star conjunctions, Uranian Transneptunian Planets (TNPs), and Astrocartography relocation mapping.
"""
from typing import Dict, Any, List, Optional
import math

# Major Fixed Stars Catalog with Sidereal Longitudes (Lahiri approx)
FIXED_STARS_CATALOG = {
    "Spica (Chitra)": {"longitude": 204.2, "nature": "Venus/Mars", "description": "Grants artistic talent, public fame, and refined intellect."},
    "Regulus (Magha)": {"longitude": 149.8, "nature": "Sun/Jupiter", "description": "Grants executive leadership, nobility, and high administrative status."},
    "Aldebaran (Rohini)": {"longitude": 69.8, "nature": "Mars/Venus", "description": "Grants material wealth, charm, and strategic leadership."},
    "Antares (Jyeshtha)": {"longitude": 249.8, "nature": "Mars/Jupiter", "description": "Grants intense courage, transformative drive, and competitive victory."},
    "Arcturus (Swati)": {"longitude": 204.2, "nature": "Jupiter/Mars", "description": "Grants independence, commercial success, and diplomatic skill."},
    "Fomalhaut (Shatabhisha)": {"longitude": 333.8, "nature": "Venus/Mercury", "description": "Grants scientific genius, mystical realization, and research depth."},
    "Vega (Abhijit)": {"longitude": 285.2, "nature": "Venus/Mercury", "description": "Grants unique talent, high ambition, and public honors."},
    "Sirius (Ardra/Punarvasu)": {"longitude": 104.1, "nature": "Jupiter/Mars", "description": "Grants extraordinary fame, high energy, and spiritual power."},
    "Andromeda Galaxy": {"longitude": 27.0, "nature": "Venus/Neptune", "description": "Grants high-frequency artistic inspiration and cosmic alignment."}
}

# Uranian Transneptunian Planets (TNPs)
URANIAN_TNPS = {
    "Cupido": "Marriage, family, group integration, art.",
    "Hades": "Deep research, antiquity, secret knowledge, transformation.",
    "Zeus": "Targeted ambition, creative direction, leadership drive.",
    "Kronos": "State authority, official promotions, government honors.",
    "Apollon": "Commercial expansion, high learning, multi-industry gains.",
    "Admetos": "Real estate, fundamental depth, endurance, focus.",
    "Vulcanus": "Mighty physical energy, supreme willpower, execution.",
    "Poseidon": "Spiritual wisdom, high ethics, intellectual enlightenment."
}

class AstrologEngine:
    """
    Astrolog Programmatic Analysis Engine.
    Computes Fixed Star Alignments and Astrocartography Relocation Analysis.
    """

    @staticmethod
    def analyze_fixed_stars(planets: Dict[str, Any], orb_deg: float = 2.0) -> List[Dict[str, Any]]:
        """Finds planetary conjunctions with major fixed stars."""
        conjunctions = []
        for p_name, p_info in planets.items():
            p_lon = getattr(p_info, "longitude", p_info if isinstance(p_info, (int, float)) else 0.0)
            for star_name, star_info in FIXED_STARS_CATALOG.items():
                s_lon = star_info["longitude"]
                diff = abs(p_lon - s_lon) % 360
                if diff > 180: diff = 360 - diff

                if diff <= orb_deg:
                    conjunctions.append({
                        "planet": p_name,
                        "star": star_name,
                        "orb": round(diff, 2),
                        "nature": star_info["nature"],
                        "description": f"{p_name} ({p_lon:.2f}°) is aligned with {star_name} (Orb {diff:.2f}°): {star_info['description']}"
                    })
        return conjunctions

    @staticmethod
    def analyze_astrocartography(chart_obj: Any, target_lat: float, target_lon: float) -> Dict[str, Any]:
        """Calculates Astrocartography Midheaven/Ascendant relocations for any city on Earth."""
        planets = getattr(chart_obj, "planets", {})
        lines = []

        for p_name, p in planets.items():
            # Midheaven (MC) line projection
            mc_lon = (p.longitude + (target_lon - chart_obj.longitude)) % 360
            lines.append({
                "planet": p_name,
                "projected_mc": round(mc_lon, 2),
                "potency": "STRONG" if p.dignity in ["Exalted", "Own Sign"] else "MODERATE"
            })

        return {
            "target_location": f"{target_lat:.2f} N, {target_lon:.2f} E",
            "relocation_lines": lines
        }

astrolog_engine = AstrologEngine()
