import pytest
from app.web3.did_vault import sovereign_natal_vault

def test_web3_decentralized_identity_did_and_zksnark_proof():
    did = sovereign_natal_vault.generate_did_for_profile("Subramanian T S", "ad1a10ab1ce7448c0d9f4b13246982e5536112d84c28f31c40a95f6841c9144c")
    assert did.startswith("did:astro:")

    zk_proof = sovereign_natal_vault.generate_zksnark_proof(did, "Ascendant is Aquarius")
    assert zk_proof["did"] == did
    assert zk_proof["proven_statement"] == "Ascendant is Aquarius"
    assert zk_proof["verified_on_chain"] is True
    assert len(zk_proof["zksnark_proof_hash"]) == 64
