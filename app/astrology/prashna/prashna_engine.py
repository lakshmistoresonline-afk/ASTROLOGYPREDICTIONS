"""
Prashna (Horary) 1-249 Seed Engine (Module 21 - Task 21.1).
Maps seed numbers (1 to 249) directly to exact KP Placidus Lagna sub-lord boundaries,
evaluates Moon aspect relationships (Applying vs Separating), and computes PrashnaResult.
"""
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime
from ..core.kp import get_kp_lords, KPEngine
from ..core.houses import RASHI_LORDS

LORDS_ORDER = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
DASHA_YEARS = {"Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7, "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17}

# Pre-computed start longitudes for all 249 KP Horary Sub-Lord seeds across 360 deg
def generate_249_kp_sublord_seeds() -> List[Dict[str, Any]]:
    seeds = []
    curr_lon = 0.0
    minutes_per_year = 800.0 / 120.0 # 6.6666... arc-minutes per dasha year

    seed_id = 1
    nak_span_deg = 13.333333333333334

    for nak_idx in range(27):
        star_lord = LORDS_ORDER[nak_idx % 9]
        start_sub_idx = LORDS_ORDER.index(star_lord)
        nak_start_lon = nak_idx * nak_span_deg

        for sub_i in range(9):
            sub_lord = LORDS_ORDER[(start_sub_idx + sub_i) % 9]
            sub_span_min = DASHA_YEARS[sub_lord] * minutes_per_year
            sub_span_deg = sub_span_min / 60.0

            sub_start_lon = nak_start_lon + sum(DASHA_YEARS[LORDS_ORDER[(start_sub_idx + k) % 9]] * minutes_per_year / 60.0 for k in range(sub_i))
            sub_end_lon = sub_start_lon + sub_span_deg

            # Check if sign boundary (every 30 deg) falls inside this sub-lord
            sign1 = int(sub_start_lon // 30)
            sign2 = int((sub_end_lon - 0.00001) // 30)

            if sign1 != sign2 and seed_id <= 249:
                # Part 1 up to sign boundary
                boundary_lon = sign2 * 30.0
                rashi1 = RASHI_LORDS[sign1 % 12]
                seeds.append({
                    "seed": seed_id,
                    "start_lon": round(sub_start_lon, 4),
                    "end_lon": round(boundary_lon, 4),
                    "sign_lord": rashi1,
                    "star_lord": star_lord,
                    "sub_lord": sub_lord
                })
                seed_id += 1

                # Part 2 after sign boundary
                rashi2 = RASHI_LORDS[sign2 % 12]
                if seed_id <= 249:
                    seeds.append({
                        "seed": seed_id,
                        "start_lon": round(boundary_lon, 4),
                        "end_lon": round(sub_end_lon, 4),
                        "sign_lord": rashi2,
                        "star_lord": star_lord,
                        "sub_lord": sub_lord
                    })
                    seed_id += 1
            else:
                if seed_id <= 249:
                    rashi = RASHI_LORDS[sign1 % 12]
                    seeds.append({
                        "seed": seed_id,
                        "start_lon": round(sub_start_lon, 4),
                        "end_lon": round(sub_end_lon, 4),
                        "sign_lord": rashi,
                        "star_lord": star_lord,
                        "sub_lord": sub_lord
                    })
                    seed_id += 1

    return seeds

KP_249_SEEDS = generate_249_kp_sublord_seeds()

@dataclass
class PrashnaResult:
    seed_number: int
    verdict: str                  # "YES" | "NO" | "CONDITIONAL"
    confidence_score: float       # 0.0 to 1.0
    estimated_window_days: int    # Days to event manifestation
    primary_significators: List[int]
    lagna_sign_lord: str
    lagna_star_lord: str
    lagna_sub_lord: str
    moon_aspect_nature: str       # "Applying (Itthasala)" | "Separating (Eshrafa)"

class PrashnaEngine:
    """
    Prashna (Horary) 1-249 Seed Engine.
    Evaluates horary queries using KP Placidus Lagna seed mapping and Moon aspect dynamics.
    """

    @staticmethod
    def get_seed_boundary(seed_number: int) -> Dict[str, Any]:
        """
        Retrieves exact longitude interval and lords for seed_number (1 to 249).
        """
        if not (1 <= seed_number <= 249):
            raise ValueError(f"INVALID_PRASHNA_SEED: Seed number must be between 1 and 249, got {seed_number}")

        # Seed lookup
        for s in KP_249_SEEDS:
            if s["seed"] == seed_number:
                return s

        return KP_249_SEEDS[seed_number - 1]

    @staticmethod
    def evaluate_query(
        seed_number: int,
        query_datetime: datetime,
        lat: float,
        lon: float,
        target_house: int = 10,
        moon_longitude: float = 96.38,
        target_cusp_longitude: float = 120.0
    ) -> PrashnaResult:
        """
        Evaluates Horary Prashna Query using KP 1-249 seed lagna and Moon aspect dynamics.
        """
        seed_info = PrashnaEngine.get_seed_boundary(seed_number)
        sign_lord = seed_info["sign_lord"]
        star_lord = seed_info["star_lord"]
        sub_lord = seed_info["sub_lord"]

        # Moon aspect to target house cusp sub lord (Applying vs Separating)
        diff = abs(moon_longitude - target_cusp_longitude) % 360.0
        if diff > 180.0: diff = 360.0 - diff

        # Applying aspect (Moon moving toward target cusp)
        is_applying = diff <= 12.0
        aspect_nature = "Applying (Itthasala)" if is_applying else "Separating (Eshrafa)"

        # Favorable KP significators for target house
        detrimental_houses = {6, 8, 12}
        sub_lord_unfavorable = sub_lord in ["Saturn", "Rahu", "Ketu"] and target_house not in [6, 8, 12]

        if is_applying and not sub_lord_unfavorable:
            verdict = "YES"
            confidence = 0.88
            window_days = int(diff * 2.5) + 3
        elif is_applying and sub_lord_unfavorable:
            verdict = "CONDITIONAL"
            confidence = 0.62
            window_days = int(diff * 4.0) + 7
        else:
            verdict = "NO"
            confidence = 0.35
            window_days = 90

        primary_significators = [1, target_house, 11]

        return PrashnaResult(
            seed_number=seed_number,
            verdict=verdict,
            confidence_score=confidence,
            estimated_window_days=window_days,
            primary_significators=primary_significators,
            lagna_sign_lord=sign_lord,
            lagna_star_lord=star_lord,
            lagna_sub_lord=sub_lord,
            moon_aspect_nature=aspect_nature
        )

prashna_engine = PrashnaEngine()
