import pytest
from app.governance.sla_monitor import sla_monitor
from app.governance.audit_logger import soc2_audit_logger

def test_governance_sla_monitor_p99_tracking():
    # Simulate API request latencies
    for lat in [12.0, 15.5, 18.2, 22.0, 35.0, 48.0, 95.0]:
        sla_monitor.record_api_latency(lat)

    comp = sla_monitor.evaluate_sla_compliance()

    assert comp["p99_latency_ms"] <= 100.0
    assert comp["sla_status"] == "COMPLIANT"
    assert comp["uptime_availability_percent"] > 99.0

def test_governance_soc2_audit_logger_hash_chain_integrity():
    # Log 3 security audit events
    soc2_audit_logger.log_security_event("API_KEY_ISSUED", "tenant_001", {"tier": "enterprise"})
    soc2_audit_logger.log_security_event("BIRTH_RECORD_ENCRYPTED", "tenant_001", {"pqc": "KYBER-1024"})
    soc2_audit_logger.log_security_event("CHART_DATA_ACCESSED", "tenant_002", {"domain": "Career"})

    is_intact = soc2_audit_logger.verify_audit_chain_integrity()
    assert is_intact is True
