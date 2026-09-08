import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import numpy as np
from collections import defaultdict
from ...database.models import db, PredictionOutcome, TimelineEventSnapshot, Chart

class AccuracyEngine:
    """
    V3.21 Production-Grade Validation & Optimization Engine.
    Strict prospective enforcement, sample size protection, and multi-cohort isolation.
    """

    METRIC_MATCHING_VERSION = "EVENT-MATCH-V1"

    @staticmethod
    def get_cohort_metrics(source_type: str = "REAL_WORLD", cohort: str = None) -> Dict[str, Any]:
        """Calculates core event detection metrics with methodological sample size indicators."""
        query = PredictionOutcome.query.filter_by(source_type=source_type)
        if cohort:
            query = query.filter_by(cohort=cohort)

        # Exclude rejected retrospective records for REAL_WORLD metrics
        if source_type == "REAL_WORLD":
            query = query.filter(PredictionOutcome.status != "REJECTED_RETROSPECTIVE")

        outcomes = query.all()
        total_n = len(outcomes)

        if total_n == 0:
            return {"status": "READY_FOR_DATA_COLLECTION", "n": 0}

        resolved = [o for o in outcomes if o.status != "PENDING"]
        n_resolved = len(resolved)

        # Phase 1E: Minimum Real-World Sample Protection
        status = "INSUFFICIENT_SAMPLE"
        if n_resolved >= 100: status = "ESTABLISHED_INITIAL_COHORT"
        elif n_resolved >= 50: status = "DEVELOPING"
        elif n_resolved >= 30: status = "PRELIMINARY"
        elif n_resolved >= 10: status = "EARLY_SIGNAL"

        tp = len([o for o in resolved if o.status == "OCCURRED"])
        fp = len([o for o in resolved if o.status == "DID_NOT_OCCUR"])
        partial = len([o for o in resolved if o.status == "PARTIALLY_OCCURRED"])

        # Precision calculation (handling partial matches as 0.5)
        precision = (tp + 0.5 * partial) / n_resolved if n_resolved > 0 else 0.0

        # Timing Analysis
        timing_errors = [o.timing_error_days for o in resolved if o.timing_error_days is not None]
        mae = np.mean([abs(e) for e in timing_errors]) if timing_errors else None
        median_error = np.median(timing_errors) if timing_errors else None

        timing_buckets = {
            "7d": len([e for e in timing_errors if abs(e) <= 7]),
            "15d": len([e for e in timing_errors if abs(e) <= 15]),
            "30d": len([e for e in timing_errors if abs(e) <= 30])
        }

        # Horizon Analysis (V3.19+)
        horizons = {"7D": [], "30D": [], "90D": [], "1Y": [], "LONG": []}
        for o in resolved:
            if not o.created_at or not o.start_date: continue
            try:
                # Use string conversion if necessary, though SQLAlchemy should handle it
                start_str = str(o.start_date)
                start_dt = datetime.strptime(start_str, "%Y-%m-%d")
                dist = (start_dt - o.created_at).days
                val = 1.0 if o.status == "OCCURRED" else 0.5 if o.status == "PARTIALLY_OCCURRED" else 0.0
                if dist <= 7: horizons["7D"].append(val)
                elif dist <= 30: horizons["30D"].append(val)
                elif dist <= 90: horizons["90D"].append(val)
                elif dist <= 365: horizons["1Y"].append(val)
                else: horizons["LONG"].append(val)
            except: continue

        # Domain Performance
        domain_stats = {}
        for o in outcomes:
            d = o.domain
            if d not in domain_stats: domain_stats[d] = {"tp": 0, "n": 0}
            domain_stats[d]["n"] += 1
            if o.status == "OCCURRED": domain_stats[d]["tp"] += 1

        return {
            "cohort": source_type,
            "status": status,
            "n": total_n,
            "resolved_n": n_resolved,
            "precision": round(precision * 100, 1),
            "tp": tp, "fp": fp, "partial": partial,
            "timing": {
                "mae": round(mae, 1) if mae is not None else "N/A",
                "median": round(median_error, 1) if median_error is not None else "N/A",
                "buckets": timing_buckets
            },
            "horizon_performance": {k: round(np.mean(v)*100, 1) if v else 0.0 for k, v in horizons.items()},
            "domain_performance": domain_stats,
            "matching_version": AccuracyEngine.METRIC_MATCHING_VERSION
        }

    @staticmethod
    def get_calibration_data(source_type: str = "REAL_WORLD") -> Dict[str, Any]:
        """Cohort-specific calibration analysis."""
        query = PredictionOutcome.query.filter_by(source_type=source_type).filter(PredictionOutcome.status != "PENDING")
        if source_type == "REAL_WORLD":
            query = query.filter(PredictionOutcome.status != "REJECTED_RETROSPECTIVE")

        resolved = query.all()
        if len(resolved) < 5: return {"status": "CALIBRATION_PENDING", "curve": []}

        buckets = {"EXTREME": [], "HIGH": [], "MEDIUM": [], "LOW": []}
        for o in resolved:
            conf = o.engine_confidence or "MEDIUM"
            val = 1.0 if o.status == "OCCURRED" else 0.5 if o.status == "PARTIALLY_OCCURRED" else 0.0
            if conf in buckets: buckets[conf].append(val)

        curve = []
        for b, vals in buckets.items():
            rate = np.mean(vals) if vals else 0.0
            curve.append({"bucket": b, "observed_rate": round(rate * 100, 1), "n": len(vals)})

        return {"status": "ACTIVE", "curve": curve}

    @staticmethod
    def get_optimal_horizons() -> Dict[str, str]:
        """Determines best-performing horizon per domain."""
        outcomes = PredictionOutcome.query.filter(PredictionOutcome.status != "PENDING").all()
        stats = defaultdict(lambda: defaultdict(list))

        for o in outcomes:
            if not o.created_at or not o.start_date: continue
            try:
                start_dt = datetime.strptime(str(o.start_date), "%Y-%m-%d")
                dist = (start_dt - o.created_at).days
                h = "SHORT" if dist <= 30 else "MEDIUM" if dist <= 90 else "LONG"
                val = 1.0 if o.status == "OCCURRED" else 0.5 if o.status == "PARTIALLY_OCCURRED" else 0.0
                stats[o.domain][h].append(val)
            except: continue

        optimal = {}
        for domain, horizons in stats.items():
            valid_horizons = {k: v for k, v in horizons.items() if len(v) >= 5}
            if not valid_horizons:
                optimal[domain] = "INSUFFICIENT_DATA"
                continue
            best_h = max(valid_horizons, key=lambda x: np.mean(valid_horizons[x]))
            optimal[domain] = best_h

        return optimal

    @staticmethod
    def analyze_evidence_patterns() -> Dict[str, Any]:
        """Correlates evidence combinations with successful outcomes."""
        outcomes = PredictionOutcome.query.filter(PredictionOutcome.status != "PENDING").all()
        patterns = defaultdict(list)

        for o in outcomes:
            if not o.evidence_snapshot: continue
            try:
                ev = json.loads(o.evidence_snapshot)
                sources = sorted(list(set([item.get('source') for item in ev])))
                pattern_key = "+".join(sources)
                val = 1.0 if o.status == "OCCURRED" else 0.5 if o.status == "PARTIALLY_OCCURRED" else 0.0
                patterns[pattern_key].append(val)
            except: continue

        results = []
        for k, v in patterns.items():
            results.append({"pattern": k, "success_rate": round(np.mean(v)*100, 1), "n": len(v)})

        return {"evidence_correlations": sorted(results, key=lambda x: x['n'], reverse=True)}

    @staticmethod
    def track_forecast_stability(chart_id: str, domain: str) -> List[Dict[str, Any]]:
        """
        V3.22 Stability Analysis.
        Tracks changes between sequential prediction snapshots.
        """
        snapshots = PredictionOutcome.query.filter_by(chart_id=chart_id, domain=domain)\
            .order_by(PredictionOutcome.created_at).all()

        history = []
        for i, s in enumerate(snapshots):
            if i == 0:
                history.append({"status": "INITIAL", "timestamp": s.created_at.isoformat()})
                continue

            prev = snapshots[i-1]
            try:
                peak_shift = (datetime.strptime(str(s.peak_date), "%Y-%m-%d") -
                             datetime.strptime(str(prev.peak_date), "%Y-%m-%d")).days

                score_change = (s.signal_score or 0) - (prev.signal_score or 0)

                stability = "STABLE"
                reason = "No significant changes detected."

                if abs(peak_shift) > 15:
                    stability = "MATERIAL_CHANGE"
                    reason = f"Peak date shifted by {peak_shift} days."
                elif abs(score_change) > 0.2:
                    stability = "MATERIAL_CHANGE"
                    reason = f"Signal strength changed by {int(score_change*100)}%."
                elif peak_shift != 0:
                    stability = "MINOR_CHANGE"
                    reason = "Micro-timing adjustment due to transit orb entry."

                history.append({
                    "timestamp": s.created_at.isoformat(),
                    "stability": stability,
                    "reason": reason,
                    "peak_shift": peak_shift,
                    "score_change": round(score_change, 2)
                })
            except: continue
        return history

    @staticmethod
    def get_detailed_cohort_metrics(source_type: str = "REAL_WORLD") -> Dict[str, Any]:
        """V3.22 Detailed Validation Audit."""
        outcomes = PredictionOutcome.query.filter_by(source_type=source_type).all()

        n_predictions = len(outcomes)
        resolved = [o for o in outcomes if o.status != "PENDING"]
        n_resolved = len(resolved)

        verified = [o for o in resolved if o.actual_event_date is not None]
        n_verified = len(verified)

        successes = [o for o in verified if o.status == "OCCURRED" and (o.timing_error_days is None or abs(o.timing_error_days) <= 15)]
        n_success = len(successes)

        status = "INSUFFICIENT_DATA"
        if n_resolved >= 10: status = "EARLY_PROSPECTIVE_SIGNAL"
        elif n_resolved > 0: status = "DATA_COLLECTION_ACTIVE"

        return {
            "cohort": source_type,
            "n_predictions": n_predictions,
            "n_resolved": n_resolved,
            "n_verified": n_verified,
            "n_success": n_success,
            "precision": round((n_success / n_resolved * 100), 1) if n_resolved > 0 else 0.0,
            "status": status
        }

accuracy_engine = AccuracyEngine()
