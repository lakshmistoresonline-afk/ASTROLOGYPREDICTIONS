import os
import json
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from ..core.models import CanonicalChart, LifeTimeline, TimelineEvent
from .engine import generate_evidence_based_predictions
from ..dasha.vimshottari import get_vimshottari_periods

class LifetimeTimelineEngine:
    """
    V3.16 Lifecycle Intelligence Engine.
    Maps a person's life from birth to future using multi-layered astrological cycles.
    """

    VERSION = "V3.16"

    @staticmethod
    def generate_lifetime_timeline(chart: CanonicalChart, profile_id: str,
                                   end_age: int = 80) -> LifeTimeline:
        birth_dt = chart.birth_datetime
        current_dt = datetime.now()
        # Cap end date by age or a reasonable future horizon
        end_dt = birth_dt + timedelta(days=int(end_age * 365.2425))

        timeline = LifeTimeline(profile_id=profile_id, birth_datetime=birth_dt)

        # 1. Generate Dasha Sequence (Core Life Structure)
        dashas = get_vimshottari_periods(chart.planets["Moon"].longitude, birth_dt)

        all_events = []

        # 2. Iterate through periods to generate domain signals
        # Optimization: Sample major life shifts (e.g., every 3 years)
        # instead of every Antardasha to maintain responsiveness.
        processed_peaks = set()

        sample_dt = birth_dt
        while sample_dt < end_dt:
            # Determine status
            status = "PAST_RECONSTRUCTION"
            if sample_dt <= current_dt <= sample_dt + timedelta(days=int(3 * 365.2425)):
                status = "PRESENT_ACTIVE"
            elif sample_dt > current_dt:
                status = "FUTURE_FORECAST"

            # Run frozen V3.15 engine at this life point
            preds = generate_evidence_based_predictions(chart, selected_date=sample_dt)

            for p in preds["predictions"]:
                # We focus on PEAK signals for the long-range timeline
                if p["prediction_strength"] == "PEAK":
                    peak_date = p["timing_window"].get("peak")
                    if not peak_date: continue

                    p_key = f"{p['domain']}_{peak_date}"
                    if p_key in processed_peaks: continue
                    processed_peaks.add(p_key)

                    age_p = LifetimeTimelineEngine._calc_age(birth_dt, peak_date)

                    event = TimelineEvent(
                        domain=p["domain"],
                        event_type=p.get("what_may_develop", "Development"),
                        event_magnitude="MAJOR",
                        start_date=p["timing_window"].get("build") or peak_date,
                        peak_date=peak_date,
                        age_at_peak=age_p,
                        signal_strength=p["prediction_strength"],
                        confidence=p["confidence"],
                        evidence_summary=p["summary"],
                        status=status,
                        # Fill optional fields
                        event_id=str(uuid.uuid4()),
                        end_date=p["timing_window"].get("decline") or peak_date,
                        age_at_start=LifetimeTimelineEngine._calc_age(birth_dt, p["timing_window"].get("build") or peak_date),
                        age_at_end=LifetimeTimelineEngine._calc_age(birth_dt, p["timing_window"].get("decline") or peak_date)
                    )
                    all_events.append(event)

            # Advance 3 years
            sample_dt += timedelta(days=int(3 * 365.2425))

        # 3. Final synthesis and sorting
        timeline.events = sorted(all_events, key=lambda x: x.peak_date)
        return timeline

    @staticmethod
    def get_life_phase_summary(timeline: LifeTimeline) -> List[Dict[str, Any]]:
        """Groups timeline into logical age-based chapters."""
        phases = []
        # Defined brackets
        brackets = [
            (0, 15, "Early Development & Education"),
            (16, 25, "Higher Knowledge & Identity"),
            (26, 45, "Career Formation & Prime Activity"),
            (46, 65, "Leadership, Status & Legacy"),
            (66, 100, "Maturity & Inner Growth")
        ]

        for start, end, label in brackets:
            bracket_events = [e for e in timeline.events if start <= e.age_at_peak <= end]
            if bracket_events:
                # Identify strongest themes in this bracket
                themes = list(set([e.domain for e in bracket_events if e.event_magnitude in ["MAJOR", "SIGNIFICANT"]]))
                phases.append({
                    "age_range": f"{start}-{end}",
                    "label": label,
                    "event_count": len(bracket_events),
                    "primary_themes": themes[:3],
                    "status": "PAST" if end < (datetime.now() - timeline.birth_datetime).days/365 else "FUTURE"
                })
        return phases

    @staticmethod
    def _map_strength_to_magnitude(strength: str) -> str:
        mapping = {"PEAK": "MAJOR", "ACTIVE": "SIGNIFICANT", "WATCH": "MODERATE", "BACKGROUND": "LOW"}
        return mapping.get(strength, "MODERATE")

    @staticmethod
    def _calc_age(birth_dt: datetime, target_date_str: str) -> float:
        try:
            target_dt = datetime.strptime(target_date_str, "%Y-%m-%d")
            return round((target_dt - birth_dt).days / 365.2425, 1)
        except:
            return 0.0

lifetime_timeline_engine = LifetimeTimelineEngine()
