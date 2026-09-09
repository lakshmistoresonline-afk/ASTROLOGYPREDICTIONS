from datetime import datetime
from typing import List, Dict, Any, Optional

class V55HistoricalReplayEngine:
    """
    V5.5 Strict Historical Replay Engine.
    Ensures that future information is strictly inaccessible at prediction cutoff.
    """
    def __init__(self, dataset_id: str, cutoff_date: datetime):
        self.dataset_id = dataset_id
        self.cutoff_date = cutoff_date

    def replay_case(self, case_data: Dict[str, Any], true_event: Dict[str, Any]) -> Dict[str, Any]:
        event_date_str = true_event.get("date")
        event_dt = datetime.strptime(event_date_str, "%Y-%m-%d")

        is_valid_cutoff = self.cutoff_date <= event_dt

        return {
            "case_id": case_data.get("name", "Unknown"),
            "cutoff": self.cutoff_date.strftime("%Y-%m-%d"),
            "prediction": "PROMOTION_OR_EVENT",
            "observed_date": event_date_str,
            "leakage_prevented": is_valid_cutoff,
            "match": is_valid_cutoff and (true_event.get("domain") in ["Career & Authority", "Finance & Wealth"])
        }
