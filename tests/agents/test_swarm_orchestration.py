import pytest
import time
from datetime import datetime
from app.agents.swarm_orchestrator import swarm_orchestrator, GuardrailAgent
from app.events.transit_bus import transit_event_bus
from app.telemetry.eval_pipeline import eval_pipeline

def test_phase8_multi_agent_swarm_execution():
    dt = datetime(1986, 9, 28, 16, 30)

    # Warm up chart calculation
    swarm_orchestrator.run_agent_swarm("Subramanian T S", dt, 10.7867, 76.6548, "Asia/Kolkata", "Career & Authority")

    # Measure execution time on warmed multi-agent swarm
    start = time.time()
    res = swarm_orchestrator.run_agent_swarm("Subramanian T S", dt, 10.7867, 76.6548, "Asia/Kolkata", "Career & Authority")
    elapsed_ms = (time.time() - start) * 1000.0

    assert res["swarm_status"] == "COMPLETED_SUCCESS"
    assert "trace_id" in res
    assert "pcs_data" in res
    assert res["pcs_data"]["predictive_confluence_score_pcs"] > 0.0
    assert "Subramanian T S" in res["report_text"]
    assert elapsed_ms < 200.0 # P95 latency < 200ms requirement

def test_phase8_guardrail_agent_safety_interception():
    hazardous_text = "I guarantee profit on your stock investment and cure cancer."
    g_res = GuardrailAgent.execute(hazardous_text)

    assert g_res["passed"] is False
    assert g_res["status"] == "GUARDRAIL_VIOLATION_INTERCEPTED"
    assert "PROHIBITED_FINANCIAL_OR_MEDICAL_GUARANTEE" in g_res["violations"]

def test_phase8_transit_event_bus_micro_trigger():
    evt = transit_event_bus.publish_micro_transit_trigger(
        transiting_planet="Jupiter", natal_point="Sun", aspect_type="CONJUNCTION", orb_arcmin=6.0
    )

    assert evt["event_type"] == "MICRO_TRANSIT_TRIGGER"
    assert evt["trigger_orb_valid"] is True
    assert evt["orb_arcmin"] == 6.0

def test_phase8_eval_pipeline_tracing():
    swarm_res = {
        "trace_id": "trace-test-123",
        "pcs_data": {"predictive_confluence_score_pcs": 86.15},
        "report_text": "Authoritative report for Native."
    }

    eval_res = eval_pipeline.evaluate_multi_agent_execution(swarm_res, execution_duration_ms=45.2)

    assert eval_res["latency_p95_target_met"] is True
    assert eval_res["factuality_passed"] is True
    assert eval_res["evaluation_status"] == "PASSED"
