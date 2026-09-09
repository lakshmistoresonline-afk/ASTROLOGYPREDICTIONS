import pytest
from app.astrology.outcomes.dataset_importer import ImportedOutcomeRecord, dataset_registry

def test_dataset_importer_quality_scoring():
    raw_valid = {
        "person_id": "p1",
        "birth_date": "1990-01-01",
        "birth_time": "12:00",
        "birth_timezone": "UTC",
        "latitude": 28.6,
        "longitude": 77.2,
        "event_type": "marriage",
        "event_date": "2020-05-05",
        "event_precision": "EXACT_DAY",
        "birth_time_precision": "EXACT_RECORDED",
        "source": "Registry Archive",
        "provenance": "Official Certificate"
    }
    rec = ImportedOutcomeRecord(raw_valid)
    assert rec.quality_class in ["HIGH_QUALITY", "MEDIUM_QUALITY"]
    assert rec.is_eligible_for_timing() is True

def test_dataset_registry_registration():
    rec = ImportedOutcomeRecord({
        "person_id": "p1", "birth_date": "1990-01-01", "birth_time": "12:00",
        "latitude": 28.6, "longitude": 77.2, "event_type": "marriage",
        "event_date": "2020-05-05", "source": "Archive", "provenance": "Cert"
    })
    meta = dataset_registry.register_dataset("ds_1", "Test DS", "v1", "REAL_OUTCOME_DATA", "Archive", "MIT", "Cert", [rec])
    assert meta["accepted_count"] == 1
    assert meta["dataset_id"] == "ds_1"
