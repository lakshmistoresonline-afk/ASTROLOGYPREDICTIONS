import pytest
from app.security.quantum_vault import quantum_vault
from app.security.tokens import token_manager

def test_quantum_vault_hybrid_encryption_and_zero_knowledge():
    birth_data = {"dob": "1986-09-28", "tob": "16:30", "latitude": 10.7867, "longitude": 76.6548}

    res = quantum_vault.encrypt_birth_record(birth_data, secret_key="test_pqc_key")

    assert res["pqc_algorithm"] == "KYBER-1024/DILITHIUM-HYBRID"
    assert len(res["encrypted_payload"]) > 10
    assert len(res["pqc_fingerprint"]) == 64 # SHA3-256 fingerprint

    # Test zero-knowledge metadata scrubbing
    scrubbed = quantum_vault.scrub_birth_metadata_zero_knowledge(birth_data)
    assert scrubbed["dob"] == "[ZERO_KNOWLEDGE_SCRUBBED]"
    assert scrubbed["latitude"] == "[ZERO_KNOWLEDGE_SCRUBBED]"

def test_ephemeral_chart_token_issuance_and_verification():
    fp = "ad1a10ab1ce7448c0d9f4b13246982e5536112d84c28f31c40a95f6841c9144c"
    token = token_manager.issue_ephemeral_chart_token(fp, ttl_seconds=3600)

    assert token.startswith("ECT.")

    is_valid, payload = token_manager.verify_ephemeral_chart_token(token)
    assert is_valid is True
    assert payload["fp"] == fp
