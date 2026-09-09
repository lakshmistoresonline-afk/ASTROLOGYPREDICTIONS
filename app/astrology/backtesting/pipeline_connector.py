from datetime import datetime
from typing import List, Dict, Any, Optional
from ..outcomes.ingestion import OutcomeIngestionPipeline, HistoricalEventRecord
from ..outcomes.taxonomy import normalize_event_type
from .leakage_guard import enforce_information_cutoff, validate_no_leakage

class V45AccuracyPipelineConnector:
    """
    V4.5 Accuracy Execution Pipeline Connector.
    Unifies ingestion, quality gates, event normalization, leakage protection, and baseline comparison.
    """
    def __init__(self):
        self.pipeline = OutcomeIngestionPipeline()
        self.readiness_state = "NO_REAL_DATA"

    def import_and_validate_record(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes a raw record through quality gates and normalization.
        """
        profile_id = raw_data.get("person_id") or raw_data.get("profile_id")
        event_type = raw_data.get("event_type")
        event_date = raw_data.get("event_date")
        source = raw_data.get("source")
        classification = raw_data.get("dataset_classification", "REAL_OUTCOME_DATA")

        rejection_reason = None
        if not profile_id:
            rejection_reason = "INSUFFICIENT_BIRTH_DATA"
        elif not event_date:
            rejection_reason = "INVALID_EVENT_DATE"
        elif not source:
            rejection_reason = "MISSING_PROVENANCE"

        if rejection_reason:
            return {"accepted": False, "reason": rejection_reason}

        record = HistoricalEventRecord(
            profile_id=str(profile_id),
            event_type=event_type,
            event_date=event_date,
            source=source,
            dataset_classification=classification,
            confidence=raw_data.get("confidence", "HIGH"),
            notes=raw_data.get("notes")
        )

        accepted = self.pipeline.ingest_record(record)
        if accepted:
            self.readiness_state = "REAL_DATA_VALIDATED"
            return {"accepted": True, "normalized_type": record.normalized_event_type}
        else:
            return {"accepted": False, "reason": "QUALITY_GATE_FAILED"}

    def run_leakage_assertion(self, prediction_as_of: datetime, event_date_str: str) -> bool:
        """
        Automated assertion proving future event data is inaccessible to prediction.
        """
        valid_cutoff = enforce_information_cutoff(prediction_as_of, event_date_str)
        return valid_cutoff

    def get_readiness_report(self) -> Dict[str, Any]:
        real_count = len(self.pipeline.get_real_outcomes())
        if real_count == 0:
            self.readiness_state = "NO_REAL_DATA"

        return {
            "readiness_state": self.readiness_state,
            "real_outcome_count": real_count,
            "rejected_count": self.pipeline.rejected_count,
            "status_message": "BLOCKED — NO REAL OUTCOME DATA" if real_count == 0 else "BACKTEST_READY"
        }

pipeline_connector = V45AccuracyPipelineConnector()
