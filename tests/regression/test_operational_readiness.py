import pytest
from app.telemetry.tracer import telemetry_tracer
from app.services.webhook_dispatcher import webhook_dispatcher
from sdk.astro_predictions_client import AstroPredictionsClient

def test_operational_telemetry_tracer():
    span_id = telemetry_tracer.start_span("job-123", "Pass_1_Data_Prep")
    assert span_id == "job-123:Pass_1_Data_Prep"

    record = telemetry_tracer.end_span(span_id, prompt_tokens=1500, completion_tokens=500)
    assert record["job_id"] == "job-123"
    assert record["total_tokens"] == 2000
    assert record["cost_usd"] > 0.0

def test_operational_webhook_dispatcher():
    # Test webhook dispatcher handles invalid endpoint gracefully with retries
    success = webhook_dispatcher.dispatch_webhook(
        webhook_url="http://localhost:9999/invalid-webhook",
        event_type="report.completed",
        job_id="job-test-456",
        payload={"status": "COMPLETED"},
        max_retries=1
    )
    assert success is False # Handled cleanly without throwing unhandled exceptions

def test_operational_sdk_instantiation():
    client = AstroPredictionsClient(base_url="http://localhost:5000", api_key="test-api-key")
    assert client.base_url == "http://localhost:5000"
    assert client.api_key == "test-api-key"
