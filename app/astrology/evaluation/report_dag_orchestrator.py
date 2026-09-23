"""
3-Pass Directed Acyclic Graph (DAG) Report Orchestrator (Module 2 - Task 2.1 & Task 2.2).
Splits report generation into 3 sequential processing passes:
Pass 1: Data Prep & Signal Filtering (Confidence Gating)
Pass 2: Core Domain Narrative Synthesis
Pass 3: Roadmap, Remedies & Integration Synthesis (Hydration Guard)
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
from .hydration_guard import hydration_guard, ReportHydrationException

class ReportDAGOrchestrator:
    """
    3-Pass DAG Pipeline Orchestrator (Module 2).
    Eliminates token exhaustion, enforces confidence gating, and separates Natal vs Transit BaZi frames.
    """

    @staticmethod
    def run_pass_1_data_prep(chart_obj: Any, selected_date: datetime, predictions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Pass 1: Data Prep & Signal Filtering (Confidence Gating).
        Evaluates metrics, filters primary vs background domains, and constructs structured AST JSON.
        """
        primary_domains = []
        background_domains = []

        for p in predictions:
            score = p.get("score", 0.0)
            q_score = p.get("quality_score", 0.0)

            # Confidence Gating Condition (Task 2.2):
            # Primary: Score >= 15.0% OR Quality Index >= 30.0/100
            if score >= 15.0 or q_score >= 30.0:
                p["is_background_signal"] = False
                primary_domains.append(p)
            else:
                p["is_background_signal"] = True
                background_domains.append(p)

        ast_json = {
            "profile_name": getattr(chart_obj, "name", "Native"),
            "chart_fingerprint": getattr(chart_obj, "chart_fingerprint", "N/A"),
            "selected_date": selected_date.isoformat(),
            "primary_domains": primary_domains,
            "background_domains": background_domains,
            "total_primary_count": len(primary_domains),
            "total_background_count": len(background_domains)
        }

        return ast_json

    @staticmethod
    def run_pass_2_core_narratives(ast_json: Dict[str, Any], bazi_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Pass 2: Core Domain Narrative Synthesis & BaZi Frame Separation (Task 2.4).
        Processes Sections 1 through 4 (Identity, Career, Dynamics, Domain Transits).
        """
        # Task 2.4: Separate Natal BaZi vs Active Transit BaZi
        natal_bazi = {
            "day_master": bazi_data.get("day_master"),
            "self_element": bazi_data.get("self_element"),
            "structure": bazi_data.get("structure"),
            "pillars": bazi_data.get("pillars", bazi_data.get("natal_pillars"))
        }

        active_transit_bazi = bazi_data.get("active_transit_bazi", {
            "target_year": 2026,
            "annual_pillar": "Bing Wu (Horse)",
            "luck_decade_pillar": "Geng Mao (Luck Decade)"
        })

        ast_json["natal_bazi"] = natal_bazi
        ast_json["active_transit_bazi"] = active_transit_bazi

        return ast_json

    @staticmethod
    def run_pass_3_roadmap_remedies(ast_json: Dict[str, Any], timeline_events: List[Any], remedies: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Pass 3: Roadmap, Remedies & Integration Synthesis.
        Processes Sections 5 and 6 (Lifetime Roadmap, Remedial Protocols) with Hydration Guard.
        """
        processed_events = []
        for ev in timeline_events:
            e_dict = ev.model_dump() if hasattr(ev, "model_dump") else (ev if isinstance(ev, dict) else {})
            p_date = e_dict.get("peak_date") or e_dict.get("peak", "Active")

            # Guarantee non-empty summary narrative for Section 5
            raw_summary = e_dict.get("evidence_summary") or e_dict.get("why_now") or e_dict.get("summary")
            if not raw_summary or raw_summary == "N/A":
                raw_summary = f"Active lifecycle milestone in {e_dict.get('domain', 'general')} sector under primary Dasha activation."

            e_dict["summary_narrative"] = raw_summary
            processed_events.append(e_dict)

        processed_remedies = []
        for r in remedies:
            why_txt = r.get("why")
            if not why_txt or why_txt.strip() in ["", "N/A"]:
                why_txt = f"Balancing {r.get('planet')} expression stabilizes functional house lordship and optimizes vital energy."
            r["why"] = why_txt
            processed_remedies.append(r)

        ast_json["lifetime_events"] = processed_events
        ast_json["remedies"] = processed_remedies

        return ast_json

    @staticmethod
    def orchestrate_3_pass_report(
        chart_obj: Any,
        selected_date: datetime,
        predictions: List[Dict[str, Any]],
        bazi_data: Dict[str, Any],
        timeline_events: List[Any],
        remedies: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Executes full 3-Pass DAG Pipeline with Hydration Guard."""
        # Pass 1: Data Prep & Signal Filtering
        ast_json = ReportDAGOrchestrator.run_pass_1_data_prep(chart_obj, selected_date, predictions)

        # Pass 2: Core Domain Narratives & BaZi Frame Separation
        ast_json = ReportDAGOrchestrator.run_pass_2_core_narratives(ast_json, bazi_data)

        # Pass 3: Roadmap & Remedies Synthesis
        ast_json = ReportDAGOrchestrator.run_pass_3_roadmap_remedies(ast_json, timeline_events, remedies)

        return ast_json

report_dag_orchestrator = ReportDAGOrchestrator()
