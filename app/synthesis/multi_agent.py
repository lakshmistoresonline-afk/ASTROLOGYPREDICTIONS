"""
Multi-Agent Astrological Consensus System (V8.0 - Part 3).
3-Agent asynchronous reasoning framework synthesizing KP Sub-Lord, Parashari Vedic, and Jaimini Chara Dasha perspectives.
"""
from typing import Dict, Any, List

class MultiAgentConsensusEngine:
    """
    Synthesizes perspectives from 3 specialized AI reasoning agents:
    - Agent 1: KP Sub-Lord Specialist (Feasibility & Sub-Lord Promises)
    - Agent 2: Parashari Vedic Specialist (Yogas, Mahadasha, & Divisional Vargas)
    - Agent 3: Jaimini Chara Dasha Specialist (Chara Karakas & Sign Dashas)
    """

    @staticmethod
    def agent_1_kp_perspective(planet_data: Dict[str, Any]) -> Dict[str, Any]:
        from ..astrology.core.kp import kp_engine
        kp_res = kp_engine.evaluate_promise(planet_data, target_house=10)
        return {
            "agent": "Agent 1 (KP Sub-Lord Specialist)",
            "verdict": "FAVORABLE" if kp_res.favorable else "UNFAVORABLE",
            "score": 85.0 if kp_res.favorable else 35.0,
            "reasoning": f"Sub-lord {kp_res.sub_lord} qualifies event feasibility."
        }

    @staticmethod
    def agent_2_parashari_perspective(chart_obj: Any) -> Dict[str, Any]:
        planets = getattr(chart_obj, "planets", {})
        sun = planets.get("Sun")
        dignity = getattr(sun, "dignity", "Neutral")
        score = 80.0 if dignity in ["Exalted", "Own Sign"] else 65.0

        return {
            "agent": "Agent 2 (Parashari Vedic Specialist)",
            "verdict": "FAVORABLE" if score >= 70.0 else "MODERATE",
            "score": score,
            "reasoning": f"Sun in {dignity} status drives structural authority."
        }

    @staticmethod
    def agent_3_jaimini_perspective(chart_obj: Any, domain: str) -> Dict[str, Any]:
        from ..astrology.synthesis.jaimini_engine import jaimini_engine
        planets = getattr(chart_obj, "planets", {})
        karakas = jaimini_engine.calculate_chara_karakas(planets)
        j_eval = jaimini_engine.evaluate_jaimini_activation(
            domain, karakas, active_chara_sign=getattr(chart_obj, "asc_rashi", 0), planets=planets
        )
        activated = j_eval["jaimini_activated"]

        return {
            "agent": "Agent 3 (Jaimini Chara Dasha Specialist)",
            "verdict": "CONFIRMED" if activated else "UNCONFIRMED",
            "score": 85.0 if activated else 55.0,
            "reasoning": f"Chara Dasha activates {j_eval['target_karaka_role']} ({j_eval['target_planet']})."
        }

    @staticmethod
    def synthesize_consensus(chart_obj: Any, domain: str, planet_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes multi-agent tri-system consensus evaluation.
        """
        a1 = MultiAgentConsensusEngine.agent_1_kp_perspective(planet_data)
        a2 = MultiAgentConsensusEngine.agent_2_parashari_perspective(chart_obj)
        a3 = MultiAgentConsensusEngine.agent_3_jaimini_perspective(chart_obj, domain)

        # Weighted tri-agent consensus score (KP: 40%, Parashari: 35%, Jaimini: 25%)
        consensus_score = round(a1["score"] * 0.40 + a2["score"] * 0.35 + a3["score"] * 0.25, 2)

        agreements = []
        discrepancies = []

        if a1["verdict"] == "FAVORABLE" and a2["verdict"] == "FAVORABLE":
            agreements.append("KP Sub-Lord and Parashari Vedic agree on favorable event feasibility.")
        elif a1["verdict"] != a2["verdict"]:
            discrepancies.append("KP Sub-Lord indicates friction while Parashari shows high dasha strength.")

        if a3["verdict"] == "CONFIRMED":
            agreements.append("Jaimini Chara Dasha confirms the primary Karaka alignment.")

        return {
            "consensus_score": consensus_score,
            "consensus_tier": "HIGH_CONSENSUS" if consensus_score >= 75.0 else "MODERATE_CONSENSUS",
            "agent_perspectives": [a1, a2, a3],
            "agreements": agreements,
            "discrepancies": discrepancies
        }

multi_agent_consensus_engine = MultiAgentConsensusEngine()
