"""
OpenTelemetry Tracing & Token Cost Observability Manager (Task 2).
Instruments DAG passes and tracks prompt_tokens, completion_tokens, and report costs.
"""
from typing import Dict, Any, Optional
import time
import logging

class TelemetryTracer:
    """
    OpenTelemetry Tracer wrapper tracking span latency and LLM token usage/costs per job_id.
    """

    # Estimated Cost per 1k Tokens (USD)
    COST_PER_1K_PROMPT = 0.0015
    COST_PER_1K_COMPLETION = 0.0020

    def __init__(self):
        self._spans = {}
        self._metrics = {}

    def start_span(self, job_id: str, span_name: str) -> str:
        span_id = f"{job_id}:{span_name}"
        self._spans[span_id] = {
            "job_id": job_id,
            "span_name": span_name,
            "start_time": time.time()
        }
        logging.info(f"[TELEMETRY] Started span '{span_name}' for job {job_id}")
        return span_id

    def end_span(self, span_id: str, prompt_tokens: int = 0, completion_tokens: int = 0) -> Dict[str, Any]:
        span = self._spans.get(span_id)
        if not span:
            return {}

        duration_ms = round((time.time() - span["start_time"]) * 1000, 2)
        cost_usd = round(
            (prompt_tokens / 1000.0 * self.COST_PER_1K_PROMPT) +
            (completion_tokens / 1000.0 * self.COST_PER_1K_COMPLETION), 5
        )

        record = {
            "job_id": span["job_id"],
            "span_name": span["span_name"],
            "duration_ms": duration_ms,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens,
            "cost_usd": cost_usd
        }

        self._metrics[span_id] = record
        logging.info(f"[TELEMETRY] Ended span '{span['span_name']}' in {duration_ms}ms | Cost: ${cost_usd:.5f}")

        # Alerting threshold check (> 15,000 ms duration)
        if duration_ms > 15000:
            logging.warning(f"[TELEMETRY ALERT] Job {span['job_id']} span '{span['span_name']}' exceeded 15s latency target ({duration_ms}ms)")

        return record

telemetry_tracer = TelemetryTracer()
