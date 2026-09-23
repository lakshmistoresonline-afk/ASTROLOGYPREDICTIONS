import pytest
from app.astrology.synthesis.prompt_router import system_prompt_router
from app.synthesis.chat_engine import astrologer_chat_engine

def test_mobile_edge_slm_prompt_routing():
    prompt = system_prompt_router.get_system_prompt("Career & Authority")
    assert "Executive" in prompt

def test_mobile_edge_slm_chat_synthesis():
    query = "What is the primary theme for my current dasha period?"
    chart_data = None

    res = astrologer_chat_engine.generate_chat_response(query, chart_data)
    assert res["safety_passed"] is True
    assert "dasha" in res["response"].lower()
