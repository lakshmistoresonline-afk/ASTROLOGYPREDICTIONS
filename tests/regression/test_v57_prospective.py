import pytest
from app.astrology.predictions.v57_prospective import V57ProspectiveLedgerRecord

def test_prospective_ledger_immutability_and_hash():
    record = V57ProspectiveLedgerRecord(
        person_id="user_123",
        domain="CAREER",
        event_type="promotion",
        prediction_text="Promotion expected",
        evidence_snapshot={"natal": "strong", "dasha": "active"}
    )

    assert record.verify_integrity() is True

    # Simulate tampering
    record.prediction_text = "Tampered prediction"
    assert record.verify_integrity() is False
