import pytest
from datetime import datetime
from app.astrology.core.calculation_config import calculate_canonical_chart
from app.astrology.synthesis.prompt_router import system_prompt_router
from app.astrology.synthesis.feature_tokenizer import ast_feature_tokenizer
from app.astrology.synthesis.remedial_synthesizer import remedial_synthesizer
from app.astrology.performance.cache_manager import ephemeris_cache_manager
from app.astrology.performance.parallel_extractor import parallel_extractor
from app.astrology.evaluation.llm_report_validator import llm_report_validator
from app.services.backoff_retry import backoff_retry_handler

def test_module3_prompt_router_and_tokenizer():
    prompt = system_prompt_router.get_system_prompt("Career & Authority")
    assert "Executive" in prompt

    persona = system_prompt_router.get_persona_type("Personality")
    assert persona == "PSYCHOLOGICAL"

    dt = datetime(1986, 9, 28, 16, 30)
    chart = calculate_canonical_chart(dt, 10.7867, 76.6548, "Asia/Kolkata")
    xml = ast_feature_tokenizer.tokenize_domain_context(chart, "Career", {"mahadasha": "Venus"})
    assert "<PRIMARY_DRIVERS>" in xml
    assert "<SECONDARY_MODIFIERS>" in xml

def test_module3_remedial_schema():
    rem = remedial_synthesizer.synthesize_remedy("Sun", "Dignity Pressure")
    assert "catalyst" in rem
    assert "behavioral_remediation" in rem
    assert "timing_window" in rem
    assert "Astrological Catalyst" in rem["formatted_schema"]

def test_module4_cache_manager_and_parallel_extractor():
    key = ephemeris_cache_manager.get_cache_key(1000000.0, 10.78, 76.65, mode="NATAL")
    ephemeris_cache_manager.set(key, {"test": 123}, cache_type="NATAL")

    cached = ephemeris_cache_manager.get(key)
    assert cached["test"] == 123

    dt = datetime(1986, 9, 28, 16, 30)
    chart = calculate_canonical_chart(dt, 10.7867, 76.6548, "Asia/Kolkata")

    features = parallel_extractor.extract_features_parallel(chart)
    assert "ashtakavarga" in features
    assert "bazi" in features
    assert "human_design" in features

def test_module5_llm_report_validator():
    dt = datetime(1986, 9, 28, 16, 30)
    chart = calculate_canonical_chart(dt, 10.7867, 76.6548, "Asia/Kolkata")

    markdown = "# Report\nLagna: Kumbha\nConfluence Match Score: 68.23%"
    qa = llm_report_validator.evaluate_report_quality(markdown, chart)
    assert qa["qa_score"] >= 90.0
    assert qa["passed"] is True

def test_module6_backoff_retry_handler():
    def dummy_success():
        return "SUCCESS"

    res = backoff_retry_handler.execute_with_retry(dummy_success, max_retries=2)
    assert res == "SUCCESS"
