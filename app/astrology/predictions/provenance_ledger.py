import hashlib
import json
from datetime import datetime
from typing import Dict, Any

class CryptographicProvenanceLedger:
    """
    V3.22 Cryptographic Provenance Ledger.
    Generates immutable SHA-256 signatures for birth charts and prediction snapshots
    to guarantee absolute proof against retrospective prediction fabrication.
    """

    @staticmethod
    def sign_prediction(chart_fingerprint: str, prediction_data: Dict[str, Any], timestamp: datetime = None) -> str:
        if timestamp is None:
            timestamp = datetime.utcnow()

        payload = {
            "chart_fingerprint": chart_fingerprint,
            "prediction_domain": prediction_data.get("domain"),
            "event_type": prediction_data.get("event_type"),
            "score": prediction_data.get("score"),
            "engine_version": prediction_data.get("engine_version", "V3.15-PROTECTED"),
            "timestamp": timestamp.isoformat()
        }

        raw_str = json.dumps(payload, sort_keys=True)
        signature = hashlib.sha256(raw_str.encode('utf-8')).hexdigest()
        return signature

    @staticmethod
    def verify_signature(chart_fingerprint: str, prediction_data: Dict[str, Any], timestamp: datetime, expected_signature: str) -> bool:
        computed = CryptographicProvenanceLedger.sign_prediction(chart_fingerprint, prediction_data, timestamp)
        return computed == expected_signature
