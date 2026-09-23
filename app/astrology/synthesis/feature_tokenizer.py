"""
Astrological Feature Tokenizer & Context Injector (Module 3 - Task 3.2).
Converts raw planet, house, and dasha data into ranked XML token tags (<PRIMARY_DRIVERS> vs <SECONDARY_MODIFIERS>).
"""
from typing import Dict, Any, List

class ASTFeatureTokenizer:
    """
    Tokenizes raw astrological data into structured, ranked XML tags for LLM context injection.
    """

    @staticmethod
    def tokenize_domain_context(chart_obj: Any, domain: str, event_prediction: Dict[str, Any]) -> str:
        """
        Structures LLM prompt inputs into standardized XML/Markdown tags:
        <PRIMARY_DRIVERS> and <SECONDARY_MODIFIERS>.
        """
        primary_drivers = []
        secondary_modifiers = []

        # 1. Active Dasha Driver
        dasha_info = getattr(chart_obj, "dasha_data", {})
        maha = event_prediction.get("mahadasha", "Active Dasha")
        primary_drivers.append(f"- Active Major Life Cycle (Mahadasha): {maha}")

        # 2. Key Karaka & House Lords
        planets = getattr(chart_obj, "planets", {})
        for p_name, p in planets.items():
            if getattr(p, "dignity", "") in ["Exalted", "Own Sign"]:
                primary_drivers.append(f"- {p_name} ({p.dignity} in House {p.house}, Functional Power: {getattr(p, 'functional_power_multiplier', 1.0)*100:.0f}%): High Promisibility")
            elif getattr(p, "house", 0) in [1, 5, 9, 10]:
                secondary_modifiers.append(f"- {p_name} in House {p.house} ({p.dignity})")

        # 3. Ashtakavarga SAV Support
        sav = getattr(chart_obj, "ashtakavarga", {}).get("SAV", [])
        if sav and len(sav) >= 12:
            max_sav_house = sav.index(max(sav)) + 1
            secondary_modifiers.append(f"- Ashtakavarga House {max_sav_house} Strength: {max(sav)} Bindus (Strong Base)")

        # Format XML Context
        p_str = "\n".join(primary_drivers) if primary_drivers else "- General Planetary Alignment"
        s_str = "\n".join(secondary_modifiers) if secondary_modifiers else "- Standard House Transits"

        xml_context = f"""<PRIMARY_DRIVERS>
{p_str}
</PRIMARY_DRIVERS>

<SECONDARY_MODIFIERS>
{s_str}
</SECONDARY_MODIFIERS>"""

        return xml_context

ast_feature_tokenizer = ASTFeatureTokenizer()
