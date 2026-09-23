"""
Backoff Retry Handler & Circuit Breaker (Module 6 - Task 6.2).
Provides exponential backoff retries and graceful quantitative fallback rendering under LLM timeout conditions.
"""
from typing import Dict, Any, Callable, Optional
import time
import logging

class BackoffRetryHandler:
    """
    Handles retries with exponential backoff and circuit breaker fallback rendering.
    """

    @staticmethod
    def execute_with_retry(
        func: Callable,
        max_retries: int = 3,
        initial_backoff: float = 0.5,
        fallback_func: Optional[Callable] = None,
        *args, **kwargs
    ) -> Any:
        backoff = initial_backoff
        for attempt in range(1, max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logging.warning(f"Attempt {attempt}/{max_retries} failed for {func.__name__}: {e}")
                if attempt == max_retries:
                    if fallback_func:
                        logging.info("Triggering Graceful Fallback Rendering Mode")
                        return fallback_func(*args, **kwargs)
                    raise e
                time.sleep(backoff)
                backoff *= 2.0

backoff_retry_handler = BackoffRetryHandler()
