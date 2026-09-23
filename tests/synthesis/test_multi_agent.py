import pytest
from datetime import datetime
from app.astrology.core.calculation_config import calculate_canonical_chart
from app.synthesis.multi_agent import multi_agent_consensus_engine

def test_multi_agent_tri_system_consensus():
    dt = datetime(1986, 9, 28, 16, 30)
    chart = calculate_canonical_chart(dt, 10.7867, 76.6548, "Asia/Kolkata")

    planet_data = {
        "name": "Jupiter",
        "star_lord": "Sun",
        "sub_lord": "Venus",
        "significators": [1, 5, 10, 11],
        "sub_lord_significators": [2, 7, 11]
    }

    consensus = multi_agent_consensus_engine.synthesize_consensus(chart, "Career & Authority", planet_data)

    assert "consensus_score" in consensus
    assert 0.0 <= consensus["consensus_score"] <= 100.0
    assert len(consensus["agent_perspectives"]) == 3
    assert "KP Sub-Lord" in consensus["agent_perspectives"][0]["agent"]
    assert "Parashari" in consensus["agent_perspectives"][1]["agent"]
    assert "Jaimini" in consensus["agent_perspectives"][2]["agent"]
    assert isinstance(consensus["agreements"], list)
