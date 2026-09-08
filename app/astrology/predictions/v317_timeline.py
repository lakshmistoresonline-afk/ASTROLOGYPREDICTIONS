import os
import json
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from ..core.models import CanonicalChart, LifeTimeline, TimelineEvent, CorroborationEvidence
from .engine import generate_evidence_based_predictions
from ..dasha.vimshottari import get_vimshottari_periods

EVENT_TAXONOMY = {
    "Career & Authority": {
        "MAJOR": "Leadership role or major professional transition",
        "SIGNIFICANT": "Promotion, job change or significant recognition",
        "MODERATE": "Incremental responsibility or professional development",
        "LOW": "Routine professional activity"
    },
    "Finance & Wealth": {
        "MAJOR": "Major asset building or significant wealth transition",
        "SIGNIFICANT": "Income expansion or significant financial decision",
        "MODERATE": "Steady accumulation or budget adjustments",
        "LOW": "Stable financial background"
    },
    "Marriage & Relationships": {
        "MAJOR": "Marriage window or major relationship transition",
        "SIGNIFICANT": "Commitment progression or partnership development",
        "MODERATE": "Relational activation or social expansion",
        "LOW": "Stable relationship phase"
    },
    "Property & Assets": {
        "MAJOR": "Property acquisition or major relocation",
        "SIGNIFICANT": "Significant renovation or property decision",
        "MODERATE": "Asset maintenance or planning",
        "LOW": "Routine domestic phase"
    }
}

class LifetimeTimelineEngineV17:
    """
    V3.17/3.22 Life Event Intelligence Engine.
    Refines the lifetime timeline with structured events, magnitude analysis, and trigger explanation.
    """

    VERSION = "V3.22"

    @staticmethod
    def generate_lifetime_timeline(chart: CanonicalChart, profile_id: str,
                                   end_age: int = 80) -> LifeTimeline:
        from ...database.models import TimelineEventSnapshot
        birth_dt = chart.birth_datetime
        current_dt = datetime.now()
        end_dt = birth_dt + timedelta(days=int(end_age * 365.2425))

        timeline = LifeTimeline(profile_id=profile_id, birth_datetime=birth_dt, engine_version=LifetimeTimelineEngineV17.VERSION)

        all_events = []
        processed_peaks = set()

        # Sampling Strategy: Every 10 years for high-performance summary (V3.22)
        sample_dt = birth_dt
        while sample_dt < end_dt:
            status = "ASTROLOGICAL_RECONSTRUCTION"
            if sample_dt <= current_dt <= sample_dt + timedelta(days=int(10 * 365.2425)):
                status = "CURRENT_INDICATION"
            elif sample_dt > current_dt:
                status = "PROSPECTIVE_FORECAST"

            # Run frozen engine
            preds = generate_evidence_based_predictions(chart, selected_date=sample_dt)

            for p in preds["predictions"]:
                if p["prediction_strength"] in ["PEAK", "ACTIVE"]:
                    peak_date = p["timing_window"].get("peak")
                    if not peak_date: continue

                    p_key = f"{p['domain']}_{peak_date}"
                    if p_key in processed_peaks: continue
                    processed_peaks.add(p_key)

                    age_p = LifetimeTimelineEngineV17._calc_age(birth_dt, peak_date)

                    # Check for verified outcome in DB
                    from ...database.models import TimelineEventSnapshot
                    verified_status = status
                    existing = TimelineEventSnapshot.query.filter_by(chart_id=profile_id, domain=p["domain"], peak_date=peak_date).first()
                    if existing and existing.matching_status != "UNKNOWN":
                        verified_status = "VERIFIED_EVENT"

                    magnitude = LifetimeTimelineEngineV17._determine_magnitude(p)

                    # Precise "Why Now" identification
                    triggers = LifetimeTimelineEngineV17._analyze_triggers(p["evidence_chain"])
                    why_now = LifetimeTimelineEngineV17._generate_why_now(p, triggers)

                    # Timing Precision (Phase 5/11)
                    precision = LifetimeTimelineEngineV17._determine_precision(current_dt, peak_date)

                    event = TimelineEvent(
                        event_id=str(uuid.uuid4()),
                        profile_id=profile_id,
                        domain=p["domain"],
                        event_type=p["event_type"],
                        event_magnitude=magnitude,
                        start_date=p["timing_window"].get("build") or peak_date,
                        peak_date=peak_date,
                        end_date=p["timing_window"].get("decline") or peak_date,
                        age_at_start=LifetimeTimelineEngineV17._calc_age(birth_dt, p["timing_window"].get("build") or peak_date),
                        age_at_peak=age_p,
                        age_at_end=LifetimeTimelineEngineV17._calc_age(birth_dt, p["timing_window"].get("decline") or peak_date),
                        signal_strength=p["prediction_strength"],
                        confidence=p["confidence"],
                        timing_precision=precision,
                        evidence_count=len(p["evidence_chain"]),
                        independent_evidence_count=len([e for e in p["evidence_chain"] if (e.level if hasattr(e, 'level') else e.get('level')) == "PRIMARY"]),
                        conflict_count=len(p.get("contradicting_factors", [])),
                        status=verified_status,
                        evidence_summary=p["summary"],
                        why_now=why_now,
                        evidence_chain=p["evidence_chain"],
                        conflicts=p.get("contradicting_factors", []),
                        engine_version=LifetimeTimelineEngineV17.VERSION
                    )
                    all_events.append(event)

            sample_dt += timedelta(days=int(10 * 365.2425))

        timeline.events = sorted(all_events, key=lambda x: x.peak_date)
        from .v316_timeline import lifetime_timeline_engine
        timeline.phases = lifetime_timeline_engine.get_life_phase_summary(timeline)

        return timeline

    @staticmethod
    def save_timeline_events(chart_id: str, events: List[TimelineEvent]):
        """Persists timeline events to DB for outcome tracking."""
        from ...database.models import db, TimelineEventSnapshot

        for e in events:
            # Check for existing
            existing = TimelineEventSnapshot.query.filter_by(id=e.event_id).first()
            if existing: continue

            snapshot = TimelineEventSnapshot(
                id=e.event_id,
                chart_id=chart_id,
                domain=e.domain,
                event_type=e.event_type,
                event_magnitude=e.event_magnitude,
                start_date=e.start_date,
                peak_date=e.peak_date,
                end_date=e.end_date,
                age_at_peak=e.age_at_peak,
                signal_strength=e.signal_strength,
                confidence=e.confidence,
                why_now=e.why_now,
                status=e.status,
                engine_version=e.engine_version
            )
            # e.evidence_chain is a list of dicts or CorroborationEvidence objects
            snapshot.evidence_snapshot = json.dumps([
                ev.model_dump() if hasattr(ev, 'model_dump') else ev
                for ev in e.evidence_chain
            ])

            db.session.add(snapshot)

        db.session.commit()

    @staticmethod
    def _determine_magnitude(p: Dict[str, Any]) -> str:
        score = p["score"]
        if score >= 85: return "MAJOR"
        if score >= 65: return "SIGNIFICANT"
        if score >= 40: return "MODERATE"
        return "LOW"

    @staticmethod
    def _determine_precision(now: datetime, peak_date_str: str) -> str:
        try:
            peak_dt = datetime.strptime(peak_date_str, "%Y-%m-%d")
            diff_days = abs((peak_dt - now).days)
            if diff_days <= 30: return "NARROW"
            if diff_days <= 365: return "MODERATE"
            return "BROAD"
        except:
            return "BROAD"

    @staticmethod
    def _analyze_triggers(evidence: List[Any]) -> Dict[str, str]:
        triggers = {}
        for e in evidence:
            # Handle both objects and dicts
            source = e.source if hasattr(e, 'source') else e.get('source')
            desc = e.description if hasattr(e, 'description') else e.get('description')
            level = e.level if hasattr(e, 'level') else e.get('level')

            if source == "NATAL_PROMISE": triggers["PROMISE"] = desc
            if source == "DASHA_ACTIVATION" and level == "PRIMARY": triggers["DASHA"] = desc
            if source == "TRANSIT_TRIGGER": triggers["TRANSIT"] = desc
            if source == "DIVISIONAL_CONFIRM": triggers["VARGA"] = desc
        return triggers

    @staticmethod
    def _generate_why_now(p: Dict[str, Any], triggers: Dict[str, str]) -> str:
        parts = []
        if "PROMISE" in triggers: parts.append("driven by the underlying natal potential")
        if "DASHA" in triggers: parts.append("activated by the current life period")
        if "TRANSIT" in triggers: parts.append("triggered by current planetary movements")
        if "VARGA" in triggers: parts.append("confirmed by specific action charts (Vargas)")

        if not parts: return "confluence of multiple astrological indicators"
        return "This window is " + ", ".join(parts[:-1]) + (" and " + parts[-1] if len(parts) > 1 else parts[0]) + "."

    @staticmethod
    def _calc_age(birth_dt: datetime, target_date_str: str) -> float:
        try:
            target_dt = datetime.strptime(target_date_str, "%Y-%m-%d")
            return round((target_dt - birth_dt).days / 365.2425, 1)
        except:
            return 0.0

lifetime_timeline_engine_v17 = LifetimeTimelineEngineV17()
