from .vimshottari import get_vimshottari_periods, calculate_dasha_balance
from datetime import datetime
from ..core.planets import PLANET_COLORS

def calculate_vimshottari(moon_longitude: float, birth_dt: datetime) -> dict:
    """Enhanced Vimshottari Dasha calculation for Dashboard 2.0."""
    balance = calculate_dasha_balance(moon_longitude)
    mahadashas_raw = get_vimshottari_periods(moon_longitude, birth_dt)

    print(f"DEBUG: Starting Vimshottari for {moon_longitude}, balance: {balance['balance_years']}")

    # Match timezone awareness of birth_dt
    if birth_dt.tzinfo:
        now = datetime.now(birth_dt.tzinfo)
    else:
        now = datetime.now()

    mahadashas = []
    current_maha = None
    current_antar = None
    current_pratyantar = None

    for m in mahadashas_raw:
        m_start = m["start"]
        m_end = m["end"]
        is_m_current = m_start <= now < m_end

        m_data = {
            "lord": m["lord"],
            "start": m_start.strftime("%d %b %Y"),
            "end": m_end.strftime("%d %b %Y"),
            "years": m["years"],
            "color": PLANET_COLORS.get(m["lord"], "#fff"),
            "is_current": is_m_current,
            "antardashas": []
        }

        if is_m_current:
            current_maha = m_data

        for a in m["antardashas"]:
            a_start = a["start"]
            a_end = a["end"]
            is_a_current = a_start <= now < a_end

            a_data = {
                "lord": a["lord"],
                "start": a_start.strftime("%d %b %Y"),
                "end": a_end.strftime("%d %b %Y"),
                "months": a["months"],
                "color": PLANET_COLORS.get(a["lord"], "#fff"),
                "is_current": is_a_current,
                "pratyantardashas": []
            }

            if is_a_current:
                current_antar = a_data

            for p in a["pratyantardashas"]:
                p_start = p["start"]
                p_end = p["end"]
                is_p_current = p_start <= now < p_end

                p_data = {
                    "lord": p["lord"],
                    "start": p_start.strftime("%d %b %Y"),
                    "end": p_end.strftime("%d %b %Y"),
                    "days": p["days"],
                    "color": PLANET_COLORS.get(p["lord"], "#fff"),
                    "is_current": is_p_current
                }

                if is_p_current:
                    current_pratyantar = p_data

                a_data["pratyantardashas"].append(p_data)

            m_data["antardashas"].append(a_data)

        mahadashas.append(m_data)

    return {
        "birth_lord": balance["lord"],
        "balance_years": balance["balance_years"],
        "balance_days": int(balance["balance_years"] * 365.2425),
        "mahadashas": mahadashas,
        "current_maha": current_maha,
        "current_antar": current_antar,
        "current_pratyantar": current_pratyantar
    }

def dasha_summary(moon_longitude: float, birth_dt: datetime) -> dict:
    data = calculate_vimshottari(moon_longitude, birth_dt)
    cm = data["current_maha"]
    ca = data["current_antar"]
    return {
        "mahadasha": cm["lord"] if cm else "N/A",
        "antardasha": ca["lord"] if ca else "N/A",
        "maha_end": cm["end"] if cm else "N/A",
        "maha_color": cm["color"] if cm else "#fff",
        "antar_color": ca["color"] if ca else "#fff"
    }
