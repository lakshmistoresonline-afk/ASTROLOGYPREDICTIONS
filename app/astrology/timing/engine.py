from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from functools import lru_cache
from ..core.models import CanonicalChart
from ..dasha.vimshottari import calculate_dasha_balance, DASHA_SEQUENCE

class TimingEngine:
    """Combines Dasha, Transit, and Ashtakavarga for event timing."""

    @staticmethod
    def calculate_dasha_activation(chart: CanonicalChart, domain_planets: List[str], target_date: datetime) -> float:
        """Score Dasha support for a domain based on activating planets."""
        from ..dasha.vimshottari import get_vimshottari_periods

        # Get current dasha lords
        moon_lon = chart.planets["Moon"].longitude
        periods = get_vimshottari_periods(moon_lon, chart.birth_datetime)

        # Find current maha and antar
        current_maha = None
        current_antar = None

        for m in periods:
            if m["start"] <= target_date <= m["end"]:
                current_maha = m["lord"]
                for a in m["antardashas"]:
                    if a["start"] <= target_date <= a["end"]:
                        current_antar = a["lord"]
                        break
                break

        score = 0.0
        if current_maha in domain_planets: score += 0.6
        if current_antar in domain_planets: score += 0.4

        return score

    @staticmethod
    def calculate_transit_support(chart: CanonicalChart, domain_houses: List[int], target_date: datetime) -> float:
        """Score Transit support based on major planets in domain houses, BAV, Kakshya, and Moorti."""
        from ..transit.engine import calculate_transit
        from ..transit.kakshya import is_kakshya_active
        from ..transit.moorti import calculate_moorti

        t_chart = calculate_transit(target_date, chart.latitude, chart.longitude, chart.timezone)

        # ... rest of logic ...
        sav = chart.ashtakavarga.get("SAV", [28] * 12)
        bav_all = chart.ashtakavarga.get("BAV", {})

        natal_rashis = {n: p.rashi for n, p in chart.planets.items()}
        natal_rashis["Lagna"] = chart.asc_rashi

        natal_moon_rashi = chart.planets["Moon"].rashi
        transit_moon_rashi = t_chart.planets["Moon"].rashi

        # Calculate general Moorti for the day
        moorti = calculate_moorti(natal_moon_rashi, transit_moon_rashi)
        moorti_mult = 1.3 if moorti["quality"] == "Highly Auspicious" else 1.1 if moorti["quality"] == "Auspicious" else 0.8

        score = 0.0
        benefics = ["Jupiter", "Venus", "Mercury"]
        malefics = ["Saturn", "Mars", "Rahu", "Ketu"]

        for p_name, p_info in t_chart.planets.items():
            t_rashi = p_info.rashi
            n_house = (t_rashi - chart.asc_rashi + 12) % 12 + 1

            if n_house in domain_houses:
                # 1. Base planet influence
                p_score = 0.2 if p_name in benefics else -0.1 if p_name in malefics else 0.0

                # 2. BAV points for the specific planet in that rashi
                bav = bav_all.get(p_name, [0] * 12)
                points = bav[t_rashi]

                # Rule: >= 5 points is very strong, < 3 is weak
                bav_mult = 1.5 if points >= 5 else 0.5 if points < 3 else 1.0

                # 3. Kakshya Activity (Phaladesh)
                # Only Sun-Sat + Lagna used for Kakshya
                is_active = True
                if p_name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
                    is_active = is_kakshya_active(p_name, t_rashi, p_info.degree, natal_rashis)

                k_mult = 1.2 if is_active else 0.7

                score += p_score * bav_mult * k_mult * moorti_mult

                # 4. Transit-to-Natal Aspect
                from ..strength.aspects import get_graha_drishti
                t_aspects = get_graha_drishti(p_name, t_rashi)
                for house in domain_houses:
                    house_rashi = (chart.asc_rashi + house - 1) % 12
                    if house_rashi in t_aspects:
                        if p_name in benefics: score += 0.1
                        if p_name in malefics: score -= 0.05

        return max(0.0, min(1.0, 0.5 + score))

    @staticmethod
    def calculate_ashtakavarga_support(chart: CanonicalChart, domain_houses: List[int]) -> float:
        """Score natal energetic support for a domain via SAV."""
        sav = chart.ashtakavarga.get("SAV", [28] * 12)
        total_points = 0
        for h in domain_houses:
            rashi = (chart.asc_rashi + h - 1) % 12
            total_points += sav[rashi]

        avg = total_points / len(domain_houses)
        return max(0.0, min(1.0, (avg - 20) / 15)) # 20 is low, 35 is very high

    @staticmethod
    def calculate_nakshatra_support(chart: CanonicalChart, target_date: datetime) -> float:
        """Personalized daily support using Tara Bala and Chandra Bala."""
        from ..core.ephemeris import get_planet_position
        from ..core.datetime import datetime_to_jd
        from ..core.nakshatra_logic import calculate_tarabala, calculate_chandrabala
        from ..core.swe_proxy import swe

        jd = datetime_to_jd(target_date, chart.timezone)
        moon_pos = get_planet_position(jd, swe.MOON)

        t_nak_idx = int(moon_pos["longitude"] / (360/27))
        t_rashi_idx = int(moon_pos["longitude"] // 30)

        n_nak_idx = chart.planets["Moon"].nakshatra.index or 0
        n_rashi_idx = chart.planets["Moon"].rashi or 0

        tara = calculate_tarabala(n_nak_idx, t_nak_idx)
        chandra = calculate_chandrabala(n_rashi_idx, t_rashi_idx)

        score = 0.5
        if tara["quality"] == "Auspicious": score += 0.2
        elif tara["quality"] == "Inauspicious": score -= 0.2

        if chandra["quality"] == "Auspicious": score += 0.1
        elif chandra["quality"] == "Inauspicious": score -= 0.1

        return max(0.0, min(1.0, score))

def get_timing_score(chart: CanonicalChart, domain_planets: List[str], domain_houses: List[int], target_date: datetime) -> Dict[str, Any]:
    engine = TimingEngine()
    d_score = engine.calculate_dasha_activation(chart, domain_planets, target_date)
    t_score = engine.calculate_transit_support(chart, domain_houses, target_date)
    av_score = engine.calculate_ashtakavarga_support(chart, domain_houses)
    nak_score = engine.calculate_nakshatra_support(chart, target_date)

    # Weighted total including daily Nakshatra energy
    total = (d_score * 0.4) + (t_score * 0.25) + (av_score * 0.15) + (nak_score * 0.2)

    return {
        "dasha_score": d_score,
        "transit_score": t_score,
        "ashtakavarga_score": av_score,
        "nakshatra_score": nak_score,
        "total_timing_score": round(total, 2),
        "label": "Strong" if total > 0.7 else "Moderate" if total > 0.4 else "Weak",
        "dasha_confirmed": d_score > 0.5,
        "transit_confirmed": t_score > 0.7
    }
