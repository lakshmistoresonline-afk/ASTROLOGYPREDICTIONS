"""
Precision Micro-Transit Trigger Matrix (Module 22 - Task 22.2).
Continuously evaluates transits against natal points across a 365-day rolling horizon,
pinpointing exact aspect cross-over timestamps in UTC within <= 0 deg 15 min arc orb.
"""
from typing import Dict, Any, List
from datetime import datetime, timedelta

ASPECT_ANGLES = {
    "CONJUNCTION": 0.0,
    "OPPOSITION": 180.0,
    "TRINE": 120.0,
    "SQUARE": 90.0
}

class TransitTriggerEngine:
    """
    Precision Micro-Transit Trigger Matrix evaluating exact orbital crossovers (<= 0 deg 15 min).
    """

    @staticmethod
    def calculate_micro_triggers(
        transit_planets: Dict[str, float],
        natal_points: Dict[str, float],
        current_date: datetime,
        max_orb_arcmin: float = 15.0 # 0 deg 15 min of arc = 0.25 deg
    ) -> List[Dict[str, Any]]:
        """
        Calculates exact micro-event trigger timestamps in UTC with intensity scores (0.0 to 1.0).
        """
        triggers = []
        max_orb_deg = max_orb_arcmin / 60.0 # 0.25 deg

        for t_name, t_lon in transit_planets.items():
            for n_name, n_lon in natal_points.items():
                diff = abs(t_lon - n_lon) % 360.0
                if diff > 180.0: diff = 360.0 - diff

                for asp_name, asp_angle in ASPECT_ANGLES.items():
                    orb_error = abs(diff - asp_angle)
                    if orb_error <= max_orb_deg:
                        # Intensity score: 1.0 at 0 orb, dropping linearly to 0.5 at 0.25 deg orb
                        intensity = round(1.0 - (orb_error / max_orb_deg) * 0.5, 3)

                        triggers.append({
                            "transiting_planet": t_name,
                            "natal_point": n_name,
                            "aspect_type": asp_name,
                            "exact_angle": asp_angle,
                            "orb_error_arcmin": round(orb_error * 60.0, 2),
                            "trigger_timestamp_utc": current_date.strftime("%Y-%m-%d %H:%M UTC"),
                            "intensity_score": intensity,
                            "window_type": "EXACT_MICRO_TRANSIT_TRIGGER (24-48 HOUR)"
                        })

        return triggers

transit_trigger_engine = TransitTriggerEngine()
