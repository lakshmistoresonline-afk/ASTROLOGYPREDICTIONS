from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from collections import defaultdict
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

        # Group by Planet + Type + NatalTarget to find local minima (peaks)
        grouped_events = defaultdict(list)
        for e in events:
            key = (e.planet, e.event_type, e.target_natal)
            grouped_events[key].append(e)

        peak_events = []
        for key, group in grouped_events.items():
            # Find event with minimum orb in this group
            # We filter for contiguous blocks (simplified: find global min in the range)
            best = min(group, key=lambda x: x.orb)
            peak_events.append(best)

        return peak_events

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
        # Scan 60 days ahead for triggers (Reduced for V3.5 Discrimination)
        transit_events = HighPrecisionTransitEngine.get_transit_events(chart, start_date, start_date + timedelta(days=60))

        # Filter for "Strong Triggers"
        # Requirement: Transit must involve a supporting planet AND hit a relevant house OR relevant natal planet
        relevant_natal_planets = {chart.house_lords.get(h) for h in houses}

        triggers = []
        for e in transit_events:
            if e.planet in supporting_planets:
                # Does it hit a relevant house?
                if e.house in houses:
                    triggers.append(e)
                # Or does it hit the lord of a relevant house?
                elif e.target_natal in relevant_natal_planets:
                    triggers.append(e)

        # Unique triggers
        unique_planets = {e.planet for e in triggers}
        trigger_count = len(unique_planets)

        # Sort by proximity
        triggers.sort(key=lambda x: x.peak_date)

        # 4. Temporal Discrimination Gate (V3.5 Hardening)
        # Only accept triggers within a tightly defined window for ACTIVE status.

        valid_peak_event = None
        for t in triggers:
            t_dt = datetime.strptime(t.peak_date, "%Y-%m-%d")
            dist = abs((t_dt - start_date).days)
            if dist <= 30: # Stricter active gate (±30 days around simulation date)
                valid_peak_event = t
                break

        if valid_peak_event:
            peak_dt = datetime.strptime(valid_peak_event.peak_date, "%Y-%m-%d")
            # 5. Manifestation Lag (V3.11): Events often manifest 7-14 days after trigger
            manifest_peak = peak_dt + timedelta(days=14)
            days_to_peak = (manifest_peak - start_date).days

            # 5. Temporal Decay Logic (V3.5)
            # We scale the bonus based on both temporal distance AND planet importance (speed)

            PLANET_IMPORTANCE = {
                "Moon": 0.15, "Mercury": 0.4, "Venus": 0.5, "Sun": 0.5,
                "Mars": 0.8, "Jupiter": 1.0, "Saturn": 1.0, "Rahu": 1.0, "Ketu": 1.0
            }

            p_imp = PLANET_IMPORTANCE.get(valid_peak_event.planet, 0.5)

            abs_dist = abs((peak_dt - start_date).days)
            if abs_dist <= 10:
                phase = "PEAK_MANIFESTATION"
                temporal_weight = 1.0
            elif abs_dist <= 30:
                phase = "NEAR_TERM_ACTIVE"
                temporal_weight = 0.60
            else:
                phase = "BUILD_UP"
                temporal_weight = 0.20

            convergence_bonus = 1.3 if trigger_count >= 2 else 1.0
            proximity_weight = temporal_weight * p_imp * convergence_bonus

            return {
                "phase": phase,
                "activation": (peak_dt - timedelta(days=20)).strftime("%Y-%m-%d"),
                "build": (peak_dt - timedelta(days=7)).strftime("%Y-%m-%d"),
                "peak": manifest_peak.strftime("%Y-%m-%d"),
                "manifestation": (manifest_peak + timedelta(days=5)).strftime("%Y-%m-%d"),
                "decline": (manifest_peak + timedelta(days=15)).strftime("%Y-%m-%d"),
                "description": f"{valid_peak_event.planet} {valid_peak_event.event_type} trigger.",
                "timing_confidence": f"{phase} ({int(proximity_weight*100)}%)",
                "proximity_weight": proximity_weight,
                "days_to_peak": days_to_peak,
                "trigger_count": trigger_count
            }
        else:
            # Fallback to Dasha-based estimation
            return {
                "phase": "STABLE_BACKGROUND",
                "activation": start_date.strftime("%Y-%m-%d"),
                "build": (start_date + timedelta(days=30)).strftime("%Y-%m-%d"),
                "peak": (start_date + timedelta(days=60)).strftime("%Y-%m-%d"),
                "manifestation": (start_date + timedelta(days=65)).strftime("%Y-%m-%d"),
                "decline": (start_date + timedelta(days=90)).strftime("%Y-%m-%d"),
                "description": "General life-period support (No immediate trigger).",
                "timing_confidence": "LOW (Dasha Only)",
                "proximity_weight": 0.0,
                "days_to_peak": 999,
                "trigger_count": 0
            }

timing_engine = TimingWindowEngine()
