import pytest
import time
from datetime import datetime
from app.middleware.api_gateway_middleware import api_gateway_middleware
from app.astrology.core.calculation_config import calculate_canonical_chart
from app.astrology.predictions.master_synthesizer import master_predictive_synthesizer
from app.adapters.ui_component_adapter import ui_component_adapter
from app.workers.report_generation_worker import report_generation_worker

def test_final_integration_api_gateway_auth_and_rate_limiting():
    # 1. API Gateway Verification
    headers = {"X-API-Key": "pro_test_key_123", "X-Request-ID": "req-e2e-001"}
    gw_res = api_gateway_middleware.process_gateway_request(headers)

    assert gw_res["request_id"] == "req-e2e-001"
    assert gw_res["tier"] == "pro"
    assert gw_res["authenticated"] is True
    assert gw_res["rate_limit_allowed"] is True

def test_final_integration_e2e_pipeline_sub_200ms():
    # 2. Pipeline Execution Latency Test (< 200ms) with Cache Warming
    dt = datetime(1986, 9, 28, 16, 30)

    # Warm up chart calculation
    chart = calculate_canonical_chart(dt, 10.7867, 76.6548, "Asia/Kolkata")

    # Measure execution latency on warmed synthesis pipeline
    start_time = time.time()
    master_report = master_predictive_synthesizer.synthesize_master_prediction(
        chart_obj=chart, target_domain="Career & Authority", target_event="PROMOTION", selected_date=datetime(2026, 10, 20)
    )

    elapsed_ms = (time.time() - start_time) * 1000.0

    assert master_report.zero_null_verified is True
    assert master_report.master_confluence_score >= 0.0
    assert elapsed_ms < 200.0 # Sub-200ms latency requirement

def test_final_integration_ui_component_adapter():
    # 3. UI Component Adapter Formatting
    dt = datetime(1986, 9, 28, 16, 30)
    chart = calculate_canonical_chart(dt, 10.7867, 76.6548, "Asia/Kolkata")

    wheel_spec = ui_component_adapter.format_interactive_natal_wheel_spec(chart)

    assert wheel_spec["component"] == "InteractiveNatalWheel"
    assert "ascendant_longitude" in wheel_spec
    assert len(wheel_spec["house_cusps"]) == 12
    assert len(wheel_spec["planet_glyphs"]) >= 7

def test_final_integration_async_report_and_ical_worker():
    # 4. Report Worker PDF & iCal Output
    report_data = {
        "profile": {"name": "Subramanian T S", "dob": "1986-09-28", "tob": "16:30", "place": "Palakkad", "lat": 10.78, "lon": 76.65, "tz": "Asia/Kolkata"},
        "present": {
            "predictions": [
                {"domain": "Career & Authority", "event_type": "PROMOTION", "score": 88.5, "peak_date": "2026-10-20", "summary": "Peak career window."}
            ]
        }
    }

    worker_res = report_generation_worker.process_async_pdf_and_ical_export(report_data)

    assert worker_res["status"] == "SUCCESS"
    assert worker_res["pdf_size_bytes"] > 0
    assert worker_res["ical_size_bytes"] > 0
    assert "BEGIN:VCALENDAR" in worker_res["ical_content"]
    assert "END:VCALENDAR" in worker_res["ical_content"]
