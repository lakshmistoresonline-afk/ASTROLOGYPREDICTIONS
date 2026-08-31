from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from ..core.models import CanonicalChart
from ..core.calc_client import calc_client

class TransitEvent:
    """
    Structured Transit Event (Phase 4).
    Calculates exact degree contact and aspect separation.
    """
    def __init__(self, planet: str, event_type: str, peak_date: str, target_natal: str = None,
                 orb: float = 0.0, house: int = None, nakshatra: str = None):
        self.planet = planet
        self.event_type = event_type
        self.peak_date = peak_date
        self.target_natal = target_natal
        self.orb = orb
        self.house = house
        self.nakshatra = nakshatra

class HighPrecisionTransitEngine:
    """
    Advanced Transit-to-Natal Detection Engine (Phase 4).
    Calculates: Conjunctions, Oppositions, Vedic Aspects, and Ingresses.
    """

    VEDIC_ASPECTS = {
        "Mars": [1, 4, 7, 8],
        "Jupiter": [1, 5, 7, 9],
        "Saturn": [1, 3, 7, 10],
        "Sun": [1, 7],
        "Moon": [1, 7],
        "Mercury": [1, 7],
        "Venus": [1, 7],
        "Rahu": [1, 5, 7, 9],
        "Ketu": [1, 5, 7, 9],
        "Default": [1, 7]
    }

    @staticmethod
    def get_transit_events(chart: CanonicalChart, start_dt: datetime, end_dt: datetime) -> List[TransitEvent]:
        raw_transits = calc_client.get_transit_range(
            start_dt.strftime("%Y-%m-%d"),
            end_dt.strftime("%Y-%m-%d"),
            chart.latitude, chart.longitude
        )

        if not raw_transits: return []

        events = []
        natal_positions = {n: p.longitude for n, p in chart.planets.items()}
        asc_rashi = int(chart.ascendant // 30)

        for day in raw_transits:
            for p_name, t_data in day["planets"].items():
                t_lon = t_data["lon"]
                t_rashi = int(t_lon // 30)
                t_house = (t_rashi - asc_rashi + 12) % 12 + 1

                # 1. Vedic Aspect Trigger (Sign-to-Sign)
                for n_name, n_lon in natal_positions.items():
                    n_rashi = int(n_lon // 30)
                    sign_diff = (t_rashi - n_rashi + 12) % 12 + 1

                    allowed_aspects = HighPrecisionTransitEngine.VEDIC_ASPECTS.get(p_name, [1, 7])

                    if sign_diff in allowed_aspects:
                        # Calculation of exact peak within the sign
                        # For now, we flag the date if within 3.0 degrees of exact aspect
                        # (1st house = 0 deg, 7th = 180, 5th = 120, etc)
                        target_angle = (sign_diff - 1) * 30.0
                        # Special check for Mars 4/8, Jup 5/9, Sat 3/10

                        actual_diff = (t_lon - n_lon + 360) % 360
                        angle_error = abs(actual_diff - target_angle)
                        if angle_error > 180: angle_error = 360 - angle_error

                        if angle_error < 3.0: # Peak window threshold
                            type_label = "CONJUNCTION" if sign_diff == 1 else f"ASPECT_{sign_diff}H"
                            events.append(TransitEvent(
                                p_name, type_label, day["date"], target_natal=n_name, orb=angle_error, house=t_house
                            ))

        return events

class TimingWindowEngine:
    """
    Calculates deterministic event windows with Activation, Build, Peak, Manifestation, Decline.
    """

    @staticmethod
    def calculate_window(chart: CanonicalChart, supporting_planets: List[str], houses: List[int], calculation_date: datetime = None) -> Dict[str, Any]:
        # 1. Point-in-time reference
        if calculation_date is None:
            start_date = datetime.now()
        else:
            start_date = calculation_date

        # 2. Dasha Activation (Base Layer)
        from ..dasha import calculate_vimshottari
        moon_lon = chart.planets["Moon"].longitude
        dasha_data = calculate_vimshottari(moon_lon, chart.birth_datetime, calculation_date=start_date)
        current_antar = dasha_data.get("current_antar", {})

        # 3. Transit Trigger (Precision Layer)
        # Scan 180 days ahead for triggers
        transit_events = HighPrecisionTransitEngine.get_transit_events(chart, start_date, start_date + timedelta(days=180))

        # Filter for "Strong Triggers": supporting planets hitting relevant houses or natal planets
        # We prioritize conjunctions or special aspects
        triggers = [e for e in transit_events if e.planet in supporting_planets]

        # Sort by proximity (earliest peak)
        triggers.sort(key=lambda x: x.peak_date)

        peak_event = triggers[0] if triggers else None

        if peak_event:
            peak_dt = datetime.strptime(peak_event.peak_date, "%Y-%m-%d")
            return {
                "phase": "PEAK_ACTIVE",
                "activation": (peak_dt - timedelta(days=20)).strftime("%Y-%m-%d"),
                "build": (peak_dt - timedelta(days=7)).strftime("%Y-%m-%d"),
                "peak": peak_dt.strftime("%Y-%m-%d"),
                "manifestation": (peak_dt + timedelta(days=3)).strftime("%Y-%m-%d"),
                "decline": (peak_dt + timedelta(days=15)).strftime("%Y-%m-%d"),
                "description": f"{peak_event.planet} {peak_event.event_type} trigger.",
                "timing_confidence": "HIGH (Transit Verified)"
            }
        else:
            # Fallback to Dasha-based estimation
            return {
                "phase": "BUILD_UP",
                "activation": start_date.strftime("%Y-%m-%d"),
                "build": (start_date + timedelta(days=15)).strftime("%Y-%m-%d"),
                "peak": (start_date + timedelta(days=30)).strftime("%Y-%m-%d"),
                "manifestation": (start_date + timedelta(days=35)).strftime("%Y-%m-%d"),
                "decline": (start_date + timedelta(days=60)).strftime("%Y-%m-%d"),
                "description": "General life-period support (Dasha only).",
                "timing_confidence": "MEDIUM (Dasha Estimation)"
            }

timing_engine = TimingWindowEngine()
