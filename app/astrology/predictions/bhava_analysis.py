from typing import Dict, List, Any
from ..core.models import CanonicalChart, DomainPrediction
from ..core.houses import RASHI_LORDS

def get_detailed_bhava_analysis(chart: CanonicalChart) -> List[Dict[str, Any]]:
    """Generate a detailed house-by-house analysis with lords, occupants, and strength."""
    analysis = []
    planets = chart.planets
    house_lords = chart.house_lords
    bhava_bala = chart.bhava_bala
    sav = chart.ashtakavarga.get("SAV", [28] * 12)
    asc_rashi = chart.asc_rashi

    house_themes = {
        1: "Self, Personality, Vitality and Life Path",
        2: "Wealth, Family, Speech and Early Education",
        3: "Courage, Siblings, Communication and Short Travels",
        4: "Home, Mother, Comforts, Vehicles and Happiness",
        5: "Intelligence, Creativity, Children and Speculation",
        6: "Health, Debts, Enemies, Service and Competition",
        7: "Marriage, Partnerships, Public Image and Social Life",
        8: "Transformation, Longevity, Secrets and Hidden Gains",
        9: "Dharma, Higher Learning, Fortune and Father",
        10: "Career, Status, Authority and Public Action",
        11: "Gains, Networks, Aspirations and Older Siblings",
        12: "Spirituality, Expenses, Foreign Lands and Moksha"
    }

    house_karakas = {
        1: "Sun", 2: "Jupiter", 3: "Mars", 4: "Moon", 5: "Jupiter",
        6: "Mars/Saturn", 7: "Venus", 8: "Saturn", 9: "Jupiter/Sun",
        10: "Saturn/Sun/Merc/Jup", 11: "Jupiter", 12: "Saturn"
    }

    # Map house to occupants
    occupants_map = {h: [] for h in range(1, 13)}
    for p_name, p_info in planets.items():
        occupants_map[p_info.house].append(p_name)

    for h_num in range(1, 13):
        lord_name = house_lords[h_num]
        lord_p = planets[lord_name]
        h_rashi = (asc_rashi + h_num - 1) % 12
        h_sav = sav[h_rashi]
        h_bala = bhava_bala.get(h_num, 0)

        from ..panchang import RASHI_NAMES
        sign_name = RASHI_NAMES[h_rashi]

        occupants = occupants_map[h_num]
        evidence = []

        # Build Interpretation
        interpretation = f"The {h_num} house, representing {house_themes[h_num]}, is ruled by {lord_name}. "

        # Lord Placement
        interpretation += f"The lord is currently placed in house {lord_p.house}, "
        if lord_p.house == h_num:
            interpretation += "which is an excellent position as the lord is in its own house, protecting its themes. "
            evidence.append(f"Lord {lord_name} is Swakshetra (Own House)")
        elif lord_p.house in [1, 4, 7, 10]:
            interpretation += "which is a powerful Kendra position, giving visibility and strength to this area of life. "
            evidence.append(f"Lord in Kendra ({lord_p.house}H)")
        elif lord_p.house in [5, 9]:
            interpretation += "which is an auspicious Trikona position, indicating natural good fortune and ease. "
            evidence.append(f"Lord in Trikona ({lord_p.house}H)")
        elif lord_p.house in [6, 8, 12]:
            interpretation += "which is a challenging 'Dusthana' house, suggesting that results in this area may come after struggle or transformation. "
            evidence.append(f"Lord in Dusthana ({lord_p.house}H)")

        # Strength Indicators
        if h_sav >= 30:
            interpretation += f"With a high SAV score of {h_sav}, this house has a strong energetic foundation to manifest its results. "
            evidence.append(f"High SAV Score: {h_sav}")
        elif h_sav < 25:
            interpretation += f"The SAV score of {h_sav} is slightly low, suggesting that manifestations here might require more conscious effort. "
            evidence.append(f"Low SAV Score: {h_sav}")

        # Advanced Strength (Vaisheshikamsha of Lord)
        if lord_p.vaisheshikamsha and lord_p.vaisheshikamsha != "None":
            interpretation += f"The lord of this house has attained {lord_p.vaisheshikamsha} status in divisional charts, indicating superior inherent quality and potential for fame. "
            evidence.append(f"Vaisheshikamsha: {lord_p.vaisheshikamsha}")

        # Occupants
        if occupants:
            interpretation += f"This house is occupied by {', '.join(occupants)}. "
            for p in occupants:
                p_data = planets[p]
                if p_data.functional_status == "Functional Benefic":
                    interpretation += f"The presence of {p} as a functional benefic brings growth and positive expansion here. "
                    evidence.append(f"Benefic {p} Presence")
                elif p_data.functional_status == "Functional Malefic":
                    interpretation += f"The presence of {p} as a functional malefic suggests hurdles or competition in this domain. "
                    evidence.append(f"Malefic {p} Presence")

                # Check for Upagrahas sitting with planets
                for upa in ["Gulika", "Mandi"]:
                    if planets.get(upa) and planets[upa].house == h_num:
                        interpretation += f"The presence of {upa} here adds a layer of karmic pressure or hidden technicalities to this house's themes. "
                        evidence.append(f"{upa} Shadow planet present")

        analysis.append({
            "house": h_num,
            "domain": house_themes[h_num],
            "lord": lord_name,
            "karaka": house_karakas[h_num],
            "occupants": occupants,
            "sign_name": sign_name,
            "strength_score": int(max(0, min(100, (h_sav / 50.0) * 100))),
            "sav": h_sav,
            "bala": h_bala,
            "interpretation": interpretation,
            "evidence": evidence
        })

    return analysis
