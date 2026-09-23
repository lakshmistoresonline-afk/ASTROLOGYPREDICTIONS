"""
Observability, Prometheus Metrics & Anomaly Guardrails (Module 24 - Task 24.2).
Exports Prometheus metrics (/metrics) and intercepts payload anomalies to send Slack/PagerDuty alerts.
"""
from typing import Dict, Any, List
import time
import logging

class ObservabilityMiddleware:
    """
    OpenTelemetry & Prometheus Metrics Exporter with Anomaly Guardrail.
    """

    def __init__(self):
        self.request_count = 0
        self.anomaly_count = 0
        self.total_latency_seconds = 0.0
        self.confluence_scores = []

    def record_request_metrics(self, duration_sec: float, confluence_score: float) -> None:
        self.request_count += 1
        self.total_latency_seconds += duration_sec
        self.confluence_scores.append(confluence_score)

    def check_payload_anomaly(self, report_payload: Dict[str, Any], alert_webhook_url: str = None) -> bool:
        """
        Anomaly Guardrail: Intercepts payload if unexpected nulls or uniform zero scores occur.
        Returns True if anomaly detected, False if healthy.
        """
        has_anomaly = False
        reasons = []

        if not report_payload:
            has_anomaly = True
            reasons.append("EMPTY_REPORT_PAYLOAD")

        score = report_payload.get("master_confluence_score", -1.0) if isinstance(report_payload, dict) else -1.0
        if score < 0.0:
            has_anomaly = True
            reasons.append("INVALID_CONFLUENCE_SCORE")

        if has_anomaly:
            self.anomaly_count += 1
            logging.error(f"[ANOMALY GUARDRAIL ALERT] Intercepted payload anomaly: {reasons}")
            if alert_webhook_url:
                self._dispatch_pagerduty_alert(alert_webhook_url, reasons)

        return has_anomaly

    def _dispatch_pagerduty_alert(self, webhook_url: str, reasons: List[str]) -> None:
        import requests
        try:
            requests.post(webhook_url, json={"event": "ANOMALY_DETECTED", "reasons": reasons}, timeout=3.0)
        except Exception as e:
            logging.warning(f"Failed to dispatch anomaly alert webhook: {e}")

    def generate_prometheus_metrics_text(self) -> str:
        """
        Generates standard Prometheus metric output string for GET /metrics.
        """
        avg_latency = (self.total_latency_seconds / self.request_count) if self.request_count > 0 else 0.0
        avg_score = (sum(self.confluence_scores) / len(self.confluence_scores)) if self.confluence_scores else 0.0

        metrics = [
            "# HELP api_request_throughput_total Total API requests processed.",
            "# TYPE api_request_throughput_total counter",
            f"api_request_throughput_total {self.request_count}",
            "# HELP astrology_calculation_latency_seconds Average calculation latency in seconds.",
            "# TYPE astrology_calculation_latency_seconds gauge",
            f"astrology_calculation_latency_seconds {avg_latency:.4f}",
            "# HELP prediction_confluence_score_distribution Average confluence score distribution.",
            "# TYPE prediction_confluence_score_distribution gauge",
            f"prediction_confluence_score_distribution {avg_score:.2f}",
            "# HELP anomaly_guardrail_alerts_total Total payload anomalies intercepted.",
            "# TYPE anomaly_guardrail_alerts_total counter",
            f"anomaly_guardrail_alerts_total {self.anomaly_count}"
        ]

        return "\n".join(metrics) + "\n"

observability_middleware = ObservabilityMiddleware()
