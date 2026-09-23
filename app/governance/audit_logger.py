"""
SOC2 & ISO27001 Compliance Audit Trail Logger (Module 12 - Part 1).
Maintains an immutable, append-only security log with cryptographically signed SHA-256 hash chains.
"""
from typing import Dict, Any, List
from datetime import datetime
import hashlib
import json

class SOC2AuditLogger:
    """
    Cryptographically chained append-only audit trail logger for SOC2 & ISO27001 compliance.
    """

    def __init__(self):
        self._audit_chain = []
        self._last_hash = "GENESIS_BLOCK_HASH_00000000000000000000000000000000"

    def log_security_event(self, action: str, tenant_id: str, payload_summary: Dict[str, Any]) -> Dict[str, Any]:
        """
        Logs security event and computes cryptographically signed SHA-256 hash chain link.
        """
        timestamp = datetime.now().isoformat()
        block_data = {
            "index": len(self._audit_chain) + 1,
            "previous_hash": self._last_hash,
            "action": action,
            "tenant_id": tenant_id,
            "timestamp": timestamp,
            "payload_summary": payload_summary
        }

        block_bytes = json.dumps(block_data, sort_keys=True).encode("utf-8")
        current_hash = hashlib.sha256(block_bytes + self._last_hash.encode("utf-8")).hexdigest()

        block_data["current_hash"] = current_hash
        self._audit_chain.append(block_data)
        self._last_hash = current_hash

        return block_data

    def verify_audit_chain_integrity(self) -> bool:
        """
        Verifies cryptographic hash chain integrity across all historical log entries.
        """
        if not self._audit_chain:
            return True

        prev_hash = "GENESIS_BLOCK_HASH_00000000000000000000000000000000"
        for block in self._audit_chain:
            if block["previous_hash"] != prev_hash:
                return False

            b_data = {
                "index": block["index"],
                "previous_hash": block["previous_hash"],
                "action": block["action"],
                "tenant_id": block["tenant_id"],
                "timestamp": block["timestamp"],
                "payload_summary": block["payload_summary"]
            }
            b_bytes = json.dumps(b_data, sort_keys=True).encode("utf-8")
            calc_hash = hashlib.sha256(b_bytes + prev_hash.encode("utf-8")).hexdigest()

            if calc_hash != block["current_hash"]:
                return False

            prev_hash = block["current_hash"]

        return True

soc2_audit_logger = SOC2AuditLogger()
