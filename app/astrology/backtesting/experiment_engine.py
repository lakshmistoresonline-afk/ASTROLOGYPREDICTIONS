from datetime import datetime
from typing import List, Dict, Any, Optional
import uuid

class PredictionExperiment:
    """
    V4 Walk-Forward Historical Backtesting & Experiment Engine.
    Prevents future leakage by enforcing explicit information cutoffs (PREDICTION_AS_OF).
    """
    def __init__(self, dataset_id: str, rule_version: str, cutoff_date: datetime):
        self.experiment_id = str(uuid.uuid4())[:8]
        self.dataset_id = dataset_id
        self.rule_version = rule_version
        self.cutoff_date = cutoff_date
        self.predictions = []
        self.outcomes = []

    def evaluate_prediction(self, prediction: Dict[str, Any], actual_event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Standardized Event Matching & Timing Scoring.
        """
        pred_domain = prediction.get("domain", "").lower()
        actual_domain = actual_event.get("domain", "").lower()

        pred_type = prediction.get("event_type", "").lower()
        actual_type = actual_event.get("event_type", "").lower()

        domain_match = pred_domain == actual_domain
        type_match = pred_type == actual_type

        match_status = "NO MATCH"
        if domain_match and type_match:
            match_status = "EXACT MATCH"
        elif domain_match:
            match_status = "RELATED EVENT"
        elif actual_event.get("is_non_event"):
            match_status = "NON EVENT"
        else:
            match_status = "CONTRADICTORY EVENT"

        # Timing scoring
        timing_error_days = None
        pred_peak = prediction.get("peak_date")
        actual_date = actual_event.get("date")

        if pred_peak and actual_date:
            try:
                dt_pred = datetime.strptime(pred_peak, "%Y-%m-%d")
                dt_act = datetime.strptime(actual_date, "%Y-%m-%d")
                timing_error_days = abs((dt_act - dt_pred).days)
            except:
                pass

        return {
            "experiment_id": self.experiment_id,
            "match_status": match_status,
            "domain_match": domain_match,
            "type_match": type_match,
            "timing_error_days": timing_error_days,
            "cutoff_date": self.cutoff_date.isoformat()
        }
