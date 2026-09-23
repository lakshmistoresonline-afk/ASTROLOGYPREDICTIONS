"""
Deep Micro-Period Dasha Engine (Module 9 - Task 9.1).
Extends Vimshottari Dasha calculations down to Level 4 (Sookshma Dasha) and Level 5 (Prana Dasha) with minute precision.
"""
from datetime import datetime, timedelta
from typing import Dict, Any, List

DASHA_ORDER = ["Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury", "Ketu", "Venus"]
DASHA_YEARS = {
    "Sun": 6, "Moon": 10, "Mars": 7, "Rahu": 18,
    "Jupiter": 16, "Saturn": 19, "Mercury": 17, "Ketu": 7, "Venus": 20
}

class DeepDashaEngine:
    """
    Calculates 5-Level Vimshottari Dasha Sub-Splits:
    Maha (Level 1) -> Antar (Level 2) -> Pratyantar (Level 3) -> Sookshma (Level 4) -> Prana (Level 5).
    """

    @staticmethod
    def calculate_sookshma_prana_dasha(
        pratyantar_lord: str,
        pratyantar_start: datetime,
        pratyantar_duration_days: float,
        target_datetime: datetime
    ) -> Dict[str, Any]:
        """
        Calculates exact Sookshma (L4) and Prana (L5) dasha sub-splits for a given target datetime.
        """
        start_idx = DASHA_ORDER.index(pratyantar_lord)
        curr_dt = pratyantar_start

        sookshma_lord = pratyantar_lord
        sookshma_start = pratyantar_start
        sookshma_end = pratyantar_start + timedelta(days=pratyantar_duration_days)

        # Level 4: Sookshma Dasha
        for i in range(9):
            lord = DASHA_ORDER[(start_idx + i) % 9]
            prop = DASHA_YEARS[lord] / 120.0
            dur_days = pratyantar_duration_days * prop
            next_dt = curr_dt + timedelta(days=dur_days)

            if curr_dt <= target_datetime < next_dt:
                sookshma_lord = lord
                sookshma_start = curr_dt
                sookshma_end = next_dt
                break
            curr_dt = next_dt

        # Level 5: Prana Dasha
        s_dur_days = (sookshma_end - sookshma_start).total_seconds() / 86400.0
        s_start_idx = DASHA_ORDER.index(sookshma_lord)
        curr_dt = sookshma_start

        prana_lord = sookshma_lord
        prana_start = sookshma_start
        prana_end = sookshma_end

        for i in range(9):
            lord = DASHA_ORDER[(s_start_idx + i) % 9]
            prop = DASHA_YEARS[lord] / 120.0
            p_dur_days = s_dur_days * prop
            next_dt = curr_dt + timedelta(days=p_dur_days)

            if curr_dt <= target_datetime < next_dt:
                prana_lord = lord
                prana_start = curr_dt
                prana_end = next_dt
                break
            curr_dt = next_dt

        return {
            "sookshma_dasha": {
                "lord": sookshma_lord,
                "start": sookshma_start.strftime("%Y-%m-%d %H:%M"),
                "end": sookshma_end.strftime("%Y-%m-%d %H:%M")
            },
            "prana_dasha": {
                "lord": prana_lord,
                "start": prana_start.strftime("%Y-%m-%d %H:%M"),
                "end": prana_end.strftime("%Y-%m-%d %H:%M")
            }
        }

deep_dasha_engine = DeepDashaEngine()
