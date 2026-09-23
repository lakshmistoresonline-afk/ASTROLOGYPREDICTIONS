import pytest
from datetime import datetime
from app.astrology.core.calculation_config import calculate_canonical_chart
from app.synthesis.chat_engine import astrologer_chat_engine
from app.synthesis.cache_optimizer import prompt_cache_optimizer

def test_synthesis_chat_engine_natal_hydrated_context():
    dt = datetime(1986, 9, 28, 16, 30)
    chart = calculate_canonical_chart(dt, 10.7867, 76.6548, "Asia/Kolkata")

    query = "How does my career trajectory look for this year?"
    res = astrologer_chat_engine.generate_chat_response(query, chart)

    assert res["safety_passed"] is True
    assert res["guardrail_triggered"] is False
    assert "career" in res["response"].lower()

def test_synthesis_chat_engine_safety_guardrail_interception():
    dt = datetime(1986, 9, 28, 16, 30)
    chart = calculate_canonical_chart(dt, 10.7867, 76.6548, "Asia/Kolkata")

    # Hazardous query attempting financial guarantee
    hazardous_query = "Can you guarantee profit on my stock purchase today?"
    res = astrologer_chat_engine.generate_chat_response(hazardous_query, chart)

    assert res["guardrail_triggered"] is True
    assert "financial advice" in res["response"]

def test_synthesis_prompt_cache_optimizer():
    prompt = "Synthesize 10th House Career Transits for Subramanian T S"
    prompt_cache_optimizer.set_cached_response(prompt, {"cached": True, "result": "PROMOTION"})

    cached = prompt_cache_optimizer.get_cached_response(prompt)
    assert cached is not None
    assert cached["cached"] is True
    assert cached["result"] == "PROMOTION"
