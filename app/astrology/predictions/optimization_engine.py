import json
from datetime import datetime, timedelta
from typing import Dict, Any, List
import pandas as pd
from ...database.models import db, PredictionOutcome, Chart
from .engine import generate_evidence_based_predictions

class V319OptimizationEngine:
    """
    V3.19 Optimization Engine.
    Evaluates new engine configurations against Training and Validation sets.
    """

    def __init__(self):
        self.training_cohort = "TRAINING"
        self.validation_cohort = "VALIDATION"
        self.holdout_cohort = "HOLDOUT"

    def run_backtest_on_resolved(self, cohort: str, engine_config: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Runs the engine at historical cutoffs for all resolved outcomes in a cohort.
        Measures if the 'Proposed' version would have correctly predicted the event.
        """
        outcomes = PredictionOutcome.query.filter_by(cohort=cohort).filter(PredictionOutcome.status != "PENDING").all()

        results = []
        for o in outcomes:
            chart = Chart.query.get(o.chart_id)
            if not chart: continue

            # Simulated Cutoff: timestamp of original prediction
            cutoff = o.created_at

            # Run engine at cutoff
            chart_obj = Chart.query.get(o.chart_id) # Need to load full obj
            # Mocking chart_obj as CanonicalChart
            from ..core.chart import calculate_chart_data
            c_data = chart.get_data()
            birth_dt = datetime.strptime(f"{c_data['birth_dob']} {c_data['birth_tob']}", "%Y-%m-%d %H:%M")
            c_obj = calculate_chart_data(birth_dt, chart.lat, chart.lon, chart.tz)

            # Generate new prediction
            preds = generate_evidence_based_predictions(c_obj, selected_date=cutoff)
            new_pred = next((p for p in preds['predictions'] if p['domain'] == o.domain), None)

            match_status = "STABLE"
            if not new_pred and o.status == "OCCURRED":
                match_status = "REGRESSION_MISS"
            elif new_pred and o.status == "DID_NOT_OCCUR":
                match_status = "REGRESSION_FALSE_POS"
            elif new_pred and o.status == "OCCURRED":
                match_status = "STABLE_MATCH"

            results.append({
                "domain": o.domain,
                "original_status": o.status,
                "new_score": new_pred['score'] if new_pred else 0,
                "match": match_status
            })

        df = pd.DataFrame(results)
        return {
            "n": len(results),
            "stable_matches": len(df[df['match'] == "STABLE_MATCH"]),
            "regressions": len(df[df['match'].str.startswith("REGRESSION")]),
            "details": results
        }

optimization_engine = V319OptimizationEngine()
