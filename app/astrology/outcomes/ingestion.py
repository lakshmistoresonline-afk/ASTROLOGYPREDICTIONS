from typing import Dict, Any, List, Optional
from datetime import datetime
from .taxonomy import normalize_event_type

VALID_DATASET_CLASSES = {
    "REAL_OUTCOME_DATA",
    "SYNTHETIC_DEVELOPMENT_DATA",
    "REFERENCE_CALCULATION_DATA"
}

class HistoricalEventRecord:
    def __init__(self, profile_id: str, event_type: str, event_date: str, source: str, dataset_classification: str = "REAL_OUTCOME_DATA", confidence: str = "HIGH", notes: Optional[str] = None):
        if dataset_classification not in VALID_DATASET_CLASSES:
            raise ValueError(f"Invalid dataset classification: {dataset_classification}")

        self.profile_id = profile_id
        self.raw_event_type = event_type
        self.normalized_event_type = normalize_event_type(event_type)
        self.event_date = event_date
        self.source = source
        self.dataset_classification = dataset_classification
        self.confidence = confidence
        self.notes = notes
        self.ingestion_timestamp = datetime.utcnow().isoformat()

    def passes_quality_gate(self) -> bool:
        """
        Data Quality Gate: Validates date format and mandatory provenance fields.
        """
        if not self.profile_id or not self.event_date or not self.source:
            return False
        try:
            datetime.strptime(self.event_date, "%Y-%m-%d")
            return True
        except ValueError:
            return False

class OutcomeIngestionPipeline:
    """
    V4.4 Production Historical Outcome Ingestion Pipeline.
    """
    def __init__(self):
        self.records: List[HistoricalEventRecord] = []
        self.rejected_count = 0

    def ingest_record(self, record: HistoricalEventRecord) -> bool:
        if record.passes_quality_gate():
            self.records.append(record)
            return True
        else:
            self.rejected_count += 1
            return False

    def get_real_outcomes(self) -> List[HistoricalEventRecord]:
        return [r for r in self.records if r.dataset_classification == "REAL_OUTCOME_DATA"]
