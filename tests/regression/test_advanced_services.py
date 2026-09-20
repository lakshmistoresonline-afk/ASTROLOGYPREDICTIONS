import pytest
from datetime import datetime
from app.astrology.core.chart import calculate_chart_data
from app.astrology.predictions.provenance_ledger import CryptographicProvenanceLedger
from app.services.medical_astrology import MedicalAstrologyService
from app.services.muhurta import BusinessMuhurtaEngine

def test_cryptographic_provenance_ledger():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_chart_data(dt, 28.6139, 77.2090, "Asia/Kolkata")
    pred_data = {"domain": "Career", "event_type": "PROMOTION", "score": 85.0}

    sig = CryptographicProvenanceLedger.sign_prediction(chart.chart_fingerprint, pred_data, dt)
    assert sig is not None
    assert len(sig) == 64 # SHA-256 hex length

    verified = CryptographicProvenanceLedger.verify_signature(chart.chart_fingerprint, pred_data, dt, sig)
    assert verified is True

def test_medical_astrology_service():
    dt = datetime(1990, 9, 10, 14, 30)
    chart = calculate_chart_data(dt, 28.6139, 77.2090, "Asia/Kolkata")
    med = MedicalAstrologyService.analyze_medical_constitution(chart)
    assert "primary_constitution" in med
    assert "vulnerabilities" in med

def test_business_muhurta_engine():
    dt = datetime(2026, 6, 1, 10, 0)
    muhurta = BusinessMuhurtaEngine.evaluate_muhurta(dt, 28.6139, 77.2090, "Asia/Kolkata")
    assert muhurta["muhurta_score"] > 0
    assert muhurta["rating"] in ["EXCELLENT", "GOOD", "MODERATE"]
