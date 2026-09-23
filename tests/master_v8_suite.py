import pytest
from datetime import datetime
from app.security.quantum_vault import quantum_vault
from app.security.tokens import token_manager
from app.resilience.self_healing import self_healing_controller
from infra.edge_routing import edge_routing_manager
from app.agents.swarm_orchestrator import swarm_orchestrator

def test_v8_quantum_security_and_zero_knowledge_vault():
    birth_data = {"dob": "1869-10-02", "tob": "08:36:00", "latitude": 21.6417, "longitude": 69.6293}
    vault_res = quantum_vault.encrypt_birth_record(birth_data, secret_key="v8_master_key")

    assert vault_res["pqc_algorithm"] == "KYBER-1024/DILITHIUM-HYBRID"
    assert vault_res["zero_knowledge_scrubbed"] is True
    assert len(vault_res["pqc_fingerprint"]) == 64

    # Ephemeral Chart Token issuance
    ect_token = token_manager.issue_ephemeral_chart_token(vault_res["pqc_fingerprint"], ttl_seconds=3600)
    assert ect_token.startswith("ECT.")

def test_v8_self_healing_circuit_breaker_failover():
    def primary_agent_slow():
        import time
        time.sleep(0.9) # Exceeds 800ms threshold
        return {"status": "PRIMARY_SUCCESS"}

    def fallback_wasm_fast():
        return {"status": "WASM_SUCCESS"}

    res = self_healing_controller.evaluate_and_route_request(
        agent_func=primary_agent_slow,
        fallback_wasm_func=fallback_wasm_fast,
        latency_threshold_ms=800.0
    )

    assert res["circuit_breaker_tripped"] is True
    assert res["fallback_mode"] == "LOCAL_WASM_PREDICTIVE_MODEL"
    assert res["status"] == "WASM_SUCCESS"

def test_v8_global_edge_anycast_routing():
    edge_res = edge_routing_manager.route_request_to_edge(21.6417, 69.6293)

    assert "SIN-CLOUDFLARE-AP-SOUTH" in edge_res["edge_pop_node"]
    assert edge_res["simulated_edge_latency_ms"] < 15.0
    assert edge_res["global_sub_15ms_target_met"] is True

def test_v8_master_unified_pipeline_end_to_end():
    dt = datetime(1986, 9, 28, 16, 30)

    # Full End-to-End Pipeline Unification Chain
    swarm_res = swarm_orchestrator.run_agent_swarm("Subramanian T S", dt, 10.7867, 76.6548, "Asia/Kolkata", "Career & Authority")

    assert swarm_res["swarm_status"] == "COMPLETED_SUCCESS"
    assert "pcs_data" in swarm_res
    assert swarm_res["pcs_data"]["predictive_confluence_score_pcs"] > 0.0
