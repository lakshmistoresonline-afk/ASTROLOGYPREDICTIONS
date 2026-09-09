import csv
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from .taxonomy import normalize_event_type

VALID_BIRTH_TIME_PRECISION = {
    "EXACT_RECORDED",
    "RECORDED_MINUTE",
    "APPROXIMATE",
    "RECTIFIED",
    "UNKNOWN"
}

VALID_EVENT_DATE_PRECISION = {
    "EXACT_DAY",
    "MONTH_ONLY",
    "YEAR_ONLY",
    "APPROXIMATE"
}

class ImportedOutcomeRecord:
    def __init__(self, raw_data: Dict[str, Any]):
        self.person_id = raw_data.get("person_id") or raw_data.get("profile_id")
        self.birth_date = raw_data.get("birth_date")
        self.birth_time = raw_data.get("birth_time")
        self.birth_timezone = raw_data.get("birth_timezone", "UTC")
        self.birth_place = raw_data.get("birth_place")
        self.latitude = raw_data.get("latitude")
        self.longitude = raw_data.get("longitude")

        self.event_type = raw_data.get("event_type")
        self.normalized_event_type = normalize_event_type(self.event_type) if self.event_type else None
        self.event_date = raw_data.get("event_date")
        self.event_precision = raw_data.get("event_precision", "EXACT_DAY")
        if self.event_precision not in VALID_EVENT_DATE_PRECISION:
            self.event_precision = "EXACT_DAY"

        self.birth_time_precision = raw_data.get("birth_time_precision", "EXACT_RECORDED")
        if self.birth_time_precision not in VALID_BIRTH_TIME_PRECISION:
            self.birth_time_precision = "UNKNOWN"

        self.source = raw_data.get("source")
        self.source_reference = raw_data.get("source_reference")
        self.provenance = raw_data.get("provenance")
        self.dataset_classification = raw_data.get("dataset_classification", "REAL_OUTCOME_DATA")

        self.quality_score, self.quality_class, self.rejection_reason = self._evaluate_quality()

    def _evaluate_quality(self) -> tuple[int, str, Optional[str]]:
        score = 100
        reasons = []

        if not self.person_id:
            score -= 40
            reasons.append("INSUFFICIENT_BIRTH_DATA")
        if not self.birth_date:
            score -= 50
            reasons.append("INVALID_BIRTH_DATE")
        if not self.birth_time or self.birth_time_precision == "UNKNOWN":
            score -= 20
            reasons.append("UNKNOWN_BIRTH_TIME")
        if self.latitude is None or self.longitude is None:
            score -= 30
            reasons.append("INVALID_LOCATION")
        if not self.event_date:
            score -= 50
            reasons.append("INVALID_EVENT_DATE")
        if not self.source or not self.provenance:
            score -= 30
            reasons.append("MISSING_PROVENANCE")

        reason_str = ";".join(reasons) if reasons else None

        if score >= 90:
            return score, "HIGH_QUALITY", reason_str
        elif score >= 70:
            return score, "MEDIUM_QUALITY", reason_str
        elif score >= 40:
            return score, "LOW_QUALITY", reason_str
        else:
            return score, "INVALID", reason_str

    def is_eligible_for_timing(self) -> bool:
        return self.quality_class in ["HIGH_QUALITY", "MEDIUM_QUALITY"] and self.event_precision == "EXACT_DAY" and self.birth_time_precision in ["EXACT_RECORDED", "RECORDED_MINUTE"]

class RealDatasetRegistry:
    def __init__(self):
        self.datasets: Dict[str, Dict[str, Any]] = {}

    def register_dataset(self, dataset_id: str, name: str, version: str, classification: str, source: str, license_str: str, provenance: str, records: List[ImportedOutcomeRecord]) -> Dict[str, Any]:
        accepted = [r for r in records if r.quality_class != "INVALID"]
        rejected = [r for r in records if r.quality_class == "INVALID"]

        quality_dist = {
            "HIGH_QUALITY": sum(1 for r in records if r.quality_class == "HIGH_QUALITY"),
            "MEDIUM_QUALITY": sum(1 for r in records if r.quality_class == "MEDIUM_QUALITY"),
            "LOW_QUALITY": sum(1 for r in records if r.quality_class == "LOW_QUALITY"),
            "INVALID": len(rejected)
        }

        dataset_meta = {
            "dataset_id": dataset_id,
            "dataset_name": name,
            "dataset_version": version,
            "classification": classification,
            "source": source,
            "license": license_str,
            "provenance": provenance,
            "record_count": len(records),
            "accepted_count": len(accepted),
            "rejected_count": len(rejected),
            "quality_distribution": quality_dist,
            "import_timestamp": datetime.utcnow().isoformat()
        }
        self.datasets[dataset_id] = dataset_meta
        return dataset_meta

dataset_registry = RealDatasetRegistry()
