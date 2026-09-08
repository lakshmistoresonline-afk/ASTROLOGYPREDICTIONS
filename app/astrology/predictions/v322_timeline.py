import os
import json
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from ..core.models import CanonicalChart, LifeTimeline, TimelineEvent, CorroborationEvidence
from .engine import generate_evidence_based_predictions

class LifetimeTimelineEngineV22:
    """
    V3.22 Lifecycle Intelligence Engine.
    Corrects temporal classification and implements horizon-dependent precision.
    """

    VERSION = "V3.22"

    @staticmethod
    def generate_lifetime_timeline(chart: CanonicalChart, profile_id: str,
                                   end_age: int = 80, generated_at: datetime = None) -> LifeTimeline:
        if generated_at is None: generated_at = datetime.now()

        birth_dt = chart.birth_datetime
        end_dt = birth_dt + timedelta(days=int(end_age * 365.2425))

        timeline = LifeTimeline(profile_id=profile_id, birth_datetime=birth_dt, engine_version=LifetimeTimelineEngineV22.VERSION)

        all_events = []
        processed_peaks = set()

        # Sampling Strategy: Balanced resolution for roadmap preview (V3.22)
        sample_dt = birth_dt
        # Optimization: Sample every 20 years for the roadmap preview.
        # This provides significant lifecycle markers while maintaining dashboard responsiveness.
        roadmap_domains = ["Career", "Finance", "Marriage", "Property", "Personality"]

        while sample_dt < end_dt:
            # Phase 2: Timeline State Correction
            # Determine status based on generated_at

            # Run engine with limited domains for performance
            preds = generate_evidence_based_predictions(chart, selected_date=sample_dt, limit_domains=roadmap_domains)

            for p in preds["predictions"]:
                if p["prediction_strength"] in ["PEAK", "ACTIVE"]:
                    peak_date_str = p["timing_window"].get("peak")
                    if not peak_date_str: continue

                    p_key = f"{p['domain']}_{peak_date_str}"
                    if p_key in processed_peaks: continue
                    processed_peaks.add(p_key)

                    peak_dt = datetime.strptime(peak_date_str, "%Y-%m-%d")
                    age_p = LifetimeTimelineEngineV22._calc_age(birth_dt, peak_date_str)

                    # Status logic (Phase 2)
                    status = "RECONSTRUCTED"
                    if peak_dt < generated_at:
                        status = "RECONSTRUCTED"
                    elif p["timing_window"].get("build") and p["timing_window"].get("decline"):
                        build_dt = datetime.strptime(p["timing_window"]["build"], "%Y-%m-%d")
                        decline_dt = datetime.strptime(p["timing_window"]["decline"], "%Y-%m-%d")
                        if build_dt <= generated_at <= decline_dt:
                            status = "CURRENT"
                        else:
                            status = "FORECAST"
                    else:
                        status = "FORECAST"

                    # Horizon-based Precision (Phase 3)
                    precision = LifetimeTimelineEngineV22._determine_precision(generated_at, peak_dt)

                    event = TimelineEvent(
                        event_id=str(uuid.uuid4()),
                        profile_id=profile_id,
                        domain=p["domain"],
                        event_type=p["event_type"],
                        event_magnitude=p["event_magnitude"],
                        start_date=p["timing_window"].get("build") or peak_date_str,
                        peak_date=peak_date_str,
                        end_date=p["timing_window"].get("decline") or peak_date_str,
                        age_at_start=LifetimeTimelineEngineV22._calc_age(birth_dt, p["timing_window"].get("build") or peak_date_str),
                        age_at_peak=age_p,
                        age_at_end=LifetimeTimelineEngineV22._calc_age(birth_dt, p["timing_window"].get("decline") or peak_date_str),
                        signal_strength=p["prediction_strength"],
                        confidence=p["confidence"],
                        timing_precision=precision,
                        status=status,
                        evidence_summary=p["summary"],
                        why_now=p["summary"],
                        evidence_chain=p["evidence_chain"],
                        engine_version=LifetimeTimelineEngineV22.VERSION
                    )
                    all_events.append(event)

            sample_dt += timedelta(days=int(20 * 365.2425))

        timeline.events = sorted(all_events, key=lambda x: x.peak_date)

        # Phase 4: Lifetime Clustering
        from .clustering import clustering_engine
        timeline_clusters = clustering_engine.cluster_predictions([e.model_dump() for e in all_events])

        # We can store clusters in a separate field or attach to timeline object
        timeline.phases = [] # Legacy phases field
        # For V3.22, we'll pass clusters separately to the template.

        return timeline

    @staticmethod
    def _determine_precision(now: datetime, peak_dt: datetime) -> str:
        diff_days = (peak_dt - now).days
        if diff_days < 0: return "HISTORICAL"
        if diff_days <= 30: return "HIGH (NARROW)"
        if diff_days <= 180: return "MODERATE (WINDOW)"
        if diff_days <= 365: return "STANDARD (MONTH)"
        return "BROAD (AGE BAND)"

    @staticmethod
    def _calc_age(birth_dt: datetime, target_date_str: str) -> float:
        try:
            target_dt = datetime.strptime(target_date_str, "%Y-%m-%d")
            return round((target_dt - birth_dt).days / 365.2425, 1)
        except:
            return 0.0

lifetime_timeline_engine_v22 = LifetimeTimelineEngineV22()
