"""
Ephemeral Chart Token (ECT) Manager (Part 1 - Task 2).
Issues short-lived, cryptographically signed Ephemeral Chart Tokens for client-side evaluation.
"""
from typing import Dict, Any, Optional, Tuple
import time
import hashlib
import hmac
import base64
import json

class TokenManager:
    """
    Issues and verifies short-lived Ephemeral Chart Tokens (ECT).
    """

    SECRET_KEY = "pqc_ect_signing_secret_999"

    @staticmethod
    def issue_ephemeral_chart_token(chart_fingerprint: str, ttl_seconds: int = 3600) -> str:
        """
        Issues signed Ephemeral Chart Token valid for ttl_seconds (default 1 hour).
        """
        expires_at = int(time.time() + ttl_seconds)
        payload = {"fp": chart_fingerprint, "exp": expires_at}
        payload_bytes = json.dumps(payload).encode("utf-8")
        payload_b64 = base64.b64encode(payload_bytes).decode("utf-8")

        sig = hmac.new(TokenManager.SECRET_KEY.encode("utf-8"), payload_b64.encode("utf-8"), hashlib.sha256).hexdigest()
        return f"ECT.{payload_b64}.{sig}"

    @staticmethod
    def verify_ephemeral_chart_token(token: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Verifies signature and expiration of an ECT token.
        """
        try:
            parts = token.split(".")
            if len(parts) != 3 or parts[0] != "ECT":
                return False, None

            payload_b64 = parts[1]
            sig = parts[2]

            expected_sig = hmac.new(TokenManager.SECRET_KEY.encode("utf-8"), payload_b64.encode("utf-8"), hashlib.sha256).hexdigest()
            if not hmac.compare_digest(expected_sig, sig):
                return False, None

            payload = json.loads(base64.b64decode(payload_b64).decode("utf-8"))
            if time.time() > payload.get("exp", 0):
                return False, None # Expired

            return True, payload
        except Exception:
            return False, None

token_manager = TokenManager()
