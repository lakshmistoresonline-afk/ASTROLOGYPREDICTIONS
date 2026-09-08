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
                 orb: float = 0.0, house: int = None, target_house: int = None, nakshatra: str = None):
        self.planet = planet
        self.event_type = event_type
        self.peak_date = peak_date
        self.target_natal = target_natal
        self.orb = orb
        self.house = house # House where transiting planet is located
        self.target_house = target_house # House being aspected
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

    _transit_cache = {}

    @staticmethod
    def get_transit_events(chart: CanonicalChart, start_dt: datetime, end_dt: datetime) -> List[TransitEvent]:
        cache_key = f"{chart.latitude}_{chart.longitude}_{start_dt.date()}_{end_dt.date()}"
        if cache_key in HighPrecisionTransitEngine._transit_cache:
            return HighPrecisionTransitEngine._transit_cache[cache_key]

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
                        target_angle = (sign_diff - 1) * 30.0
                        actual_diff = (t_lon - n_lon + 360) % 360
                        angle_error = abs(actual_diff - target_angle)
                        if angle_error > 180: angle_error = 360 - angle_error

                        if angle_error < 3.0: # Peak window threshold
                            type_label = "CONJUNCTION" if sign_diff == 1 else f"ASPECT_{sign_diff}H"
                            target_h = (t_house + sign_diff - 2) % 12 + 1

                            events.append(TransitEvent(
                                p_name, type_label, day["date"], target_natal=n_name, orb=angle_error,
                                house=t_house, target_house=target_h
                            ))

        # Group by Planet + Type + NatalTarget to find local minima (peaks)
        grouped_events = defaultdict(list)
        for e in events:
            key = (e.planet, e.event_type, e.target_natal)
            grouped_events[key].append(e)

        peak_events = []
        for key, group in grouped_events.items():
            best = min(group, key=lambda x: x.orb)
            peak_events.append(best)

        HighPrecisionTransitEngine._transit_cache[cache_key] = peak_events
        return peak_events

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
                            # Calculate the house being hit by this aspect
                            # Sign-based house index:
                            target_h = (t_house + sign_diff - 2) % 12 + 1

                            events.append(TransitEvent(
                                p_name, type_label, day["date"], target_natal=n_name, orb=angle_error,
                                house=t_house, target_house=target_h
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

    # Domain-Specific Calibration (V3.14)
    MANIFESTATION_LAG = {
        "Career & Authority": 28,
        "Education & Knowledge": 7,
        "Finance & Wealth": 14,
        "Business & Enterprise": 14,
        "Fame & Reputation": 14,
        "Default": 14
    }

    @staticmethod
    def calculate_window(chart: CanonicalChart, supporting_planets: List[str], houses: List[int],
                         calculation_date: datetime = None, domain: str = "Default") -> Dict[str, Any]:
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

        # Dasha Transition Detection (V3.14)
        transition_bonus = 1.0
        transition_phase = "STABLE"
        if current_antar:
            antar_start_dt = datetime.strptime(current_antar["start"], "%d %b %Y")
            antar_end_dt = datetime.strptime(current_antar["end"], "%d %b %Y")

            days_from_start = (start_date - antar_start_dt).days
            days_to_end = (antar_end_dt - start_date).days

            if 0 <= days_from_start <= 30:
                transition_phase = "ACTIVATION"
                transition_bonus = 1.0 # V3.12 Baseline Reversion: No score bonus
            elif 0 <= days_to_end <= 15:
                transition_phase = "TRANSITION_PREP"
                transition_bonus = 1.0

        # 3. Transit Trigger (Precision Layer)
        # Scan 60 days ahead for triggers
        transit_events = HighPrecisionTransitEngine.get_transit_events(chart, start_date, start_date + timedelta(days=60))

        # Filter for "Strong Triggers"
        relevant_natal_planets = {chart.house_lords.get(h) for h in houses}
        antar_lord = current_antar.get("lord")
        maha_lord = dasha_data.get("current_maha", {}).get("lord")

        # Resolve Proxies (V3.14)
        from ..predictions.framework import CorroborationEngine
        antar_proxies = CorroborationEngine.resolve_node_proxy(antar_lord, chart) if antar_lord else []
        maha_proxies = CorroborationEngine.resolve_node_proxy(maha_lord, chart) if maha_lord else []

        triggers = []
        for e in transit_events:
            # V3.12: Expanded supporting planets to include Dasha Lords (Direct)
            effective_supporting = set(supporting_planets) | {antar_lord, maha_lord}

            if e.planet in effective_supporting:
                # Filter weak Moon transits (V3.14)
                if e.planet == "Moon" and e.planet != antar_lord:
                    continue

                # Does it hit a relevant house? (V3.14 Hardened)
                is_direct_hit = e.house in houses
                is_aspect_hit = e.target_house in houses if hasattr(e, 'target_house') else False

                # Aspect hit is considered for Major Planets or the Antar Lord (V3.14)
                if is_aspect_hit and e.planet not in ["Jupiter", "Saturn", "Rahu", "Ketu", "Mars", antar_lord]:
                    is_aspect_hit = False

                # V3.15 Aspect Filtering: Restrict Saturn/Mars but preserve primary 7th aspect
                if is_aspect_hit:
                    if e.planet == "Saturn" and e.event_type not in ["ASPECT_3H", "ASPECT_10H", "ASPECT_7H"]:
                        is_aspect_hit = False
                    elif e.planet == "Mars" and e.event_type not in ["ASPECT_4H", "ASPECT_8H", "ASPECT_7H"]:
                        is_aspect_hit = False

                is_hit = is_direct_hit or is_aspect_hit
                is_lord_hit = e.target_natal in relevant_natal_planets
                # V3.12: High-impact trigger if Antar Lord hits a relevant target
                is_antar_trigger = e.planet == antar_lord and (is_hit or is_lord_hit)

                if is_hit or is_lord_hit or is_antar_trigger:
                    triggers.append(e)

        # Unique triggers
        unique_planets = {e.planet for e in triggers}
        trigger_count = len(unique_planets)

        # Sort by proximity
        triggers.sort(key=lambda x: x.peak_date)

        # 4. Temporal Discrimination Gate (V3.5 Hardening)
        valid_peak_event = None
        for t in triggers:
            t_dt = datetime.strptime(t.peak_date, "%Y-%m-%d")
            dist = abs((t_dt - start_date).days)
            if dist <= 30:
                valid_peak_event = t
                break

        if valid_peak_event:
            peak_dt = datetime.strptime(valid_peak_event.peak_date, "%Y-%m-%d")

            # 5. Domain-Specific Manifestation Lag (V3.14)
            lag_days = TimingWindowEngine.MANIFESTATION_LAG.get(domain, 14)
            manifest_peak = peak_dt + timedelta(days=lag_days)
            days_to_peak = (manifest_peak - start_date).days

            PLANET_IMPORTANCE = {
                "Moon": 0.15, "Mercury": 0.4, "Venus": 0.5, "Sun": 0.5,
                "Mars": 0.8, "Jupiter": 1.0, "Saturn": 1.0, "Rahu": 1.1, "Ketu": 1.1 # Boosted nodes (V3.14)
            }

            p_imp = PLANET_IMPORTANCE.get(valid_peak_event.planet, 0.5)

            # V3.15 Trigger Weighting: Increase Antardasha Lord importance on critical targets
            if valid_peak_event.planet == antar_lord:
                if valid_peak_event.target_natal == antar_lord:
                    p_imp *= 1.25 # Direct return boost
                elif valid_peak_event.target_natal == chart.planets.get(antar_lord).dispositor:
                    p_imp *= 1.15 # Dispositor trigger boost

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
                "transition_status": transition_phase,
                "activation": (peak_dt - timedelta(days=20)).strftime("%Y-%m-%d"),
                "build": (peak_dt - timedelta(days=7)).strftime("%Y-%m-%d"),
                "peak": manifest_peak.strftime("%Y-%m-%d"),
                "manifestation": (manifest_peak + timedelta(days=5)).strftime("%Y-%m-%d"),
                "decline": (manifest_peak + timedelta(days=15)).strftime("%Y-%m-%d"),
                "description": f"{valid_peak_event.planet} {valid_peak_event.event_type} trigger ({transition_phase}).",
                "timing_confidence": f"{phase} ({int(proximity_weight*100)}%)",
                "proximity_weight": proximity_weight,
                "days_to_peak": days_to_peak,
                "trigger_count": trigger_count
            }
        else:
            # Fallback to Dasha-based estimation
            return {
                "phase": "STABLE_BACKGROUND",
                "transition_status": transition_phase,
                "activation": start_date.strftime("%Y-%m-%d"),
                "build": (start_date + timedelta(days=30)).strftime("%Y-%m-%d"),
                "peak": (start_date + timedelta(days=60)).strftime("%Y-%m-%d"),
                "manifestation": (start_date + timedelta(days=65)).strftime("%Y-%m-%d"),
                "decline": (start_date + timedelta(days=90)).strftime("%Y-%m-%d"),
                "description": f"General life-period support ({transition_phase}).",
                "timing_confidence": "LOW (Dasha Only)",
                "proximity_weight": 0.0,
                "days_to_peak": 999,
                "trigger_count": 0
            }

timing_engine = TimingWindowEngine()
