"""
Enterprise Rate Limiter & Token Bucket Engine (Part 1 - Task 1).
Supports tier-based rate limits: Free (60 req/min), Pro (600 req/min), Enterprise (Unlimited).
Adds headers: X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset.
"""
from typing import Dict, Any, Tuple
import time

TIER_LIMITS = {
    "free": 60,         # 60 req/min
    "pro": 600,        # 600 req/min
    "enterprise": 999999 # Unlimited
}

_bucket_store = {}

class RateLimiter:
    """
    Async token-bucket rate limiter tracking request capacity per tenant ID.
    """

    @staticmethod
    def evaluate_rate_limit(tenant_id: str, tier: str = "free") -> Tuple[bool, Dict[str, str]]:
        """
        Evaluates token bucket for tenant_id and tier.
        Returns (is_allowed, headers_dict).
        """
        now = time.time()
        max_capacity = TIER_LIMITS.get(tier.lower(), 60)
        window_size_sec = 60.0

        # Retrieve or initialize bucket
        bucket = _bucket_store.get(tenant_id, {"tokens": max_capacity, "last_refill": now})

        # Refill tokens based on elapsed time
        elapsed = now - bucket["last_refill"]
        refill_rate = max_capacity / window_size_sec
        bucket["tokens"] = min(max_capacity, bucket["tokens"] + elapsed * refill_rate)
        bucket["last_refill"] = now

        is_allowed = bucket["tokens"] >= 1.0

        if is_allowed:
            bucket["tokens"] -= 1.0

        _bucket_store[tenant_id] = bucket

        remaining = int(bucket["tokens"])
        reset_time = int(now + window_size_sec)

        headers = {
            "X-RateLimit-Limit": str(max_capacity),
            "X-RateLimit-Remaining": str(max(0, remaining)),
            "X-RateLimit-Reset": str(reset_time)
        }

        return is_allowed, headers

rate_limiter = RateLimiter()
