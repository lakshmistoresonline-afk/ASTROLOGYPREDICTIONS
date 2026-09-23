from typing import Dict, List, Any
from datetime import date

# Stems and Branches
STEMS = ["Jia", "Yi", "Bing", "Ding", "Wu", "Ji", "Geng", "Xin", "Ren", "Gui"]
BRANCHES = ["Zi", "Chou", "Yin", "Mao", "Chen", "Si", "Wu", "Wei", "Shen", "You", "Xu", "Hai"]
ANIMALS = ["Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake", "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig"]
ELEMENTS = ["Yang Wood", "Yin Wood", "Yang Fire", "Yin Fire", "Yang Earth", "Yin Earth", "Yang Metal", "Yin Metal", "Yang Water", "Yin Water"]

def calculate_bazi_pillars(year: int, month: int, day: int, hour: int, target_year: int = 2026) -> Dict[str, Any]:
    """
    Four Pillars of Destiny (Bazi) calculation.
    Explicitly separates Natal Four Pillars from Active Transit BaZi (Annual & Luck Pillars).
    """
    # 1. NATAL BAZI FOUR PILLARS
    # Year Pillar (1984 was Jia Zi)
    y_offset = (year - 1984) % 60
    y_stem = STEMS[y_offset % 10]
    y_branch = BRANCHES[y_offset % 12]

    # Day Pillar (Reference: 2000-01-01 was Geng Chen)
    d1 = date(2000, 1, 1)
    d2 = date(year, month, day)
    days_diff = (d2 - d1).days

    d_offset = (days_diff + 16) % 60 # 16 offset for Geng Chen
    d_stem = STEMS[d_offset % 10]
    d_branch = BRANCHES[d_offset % 12]

    day_master = d_stem
    element = ELEMENTS[STEMS.index(d_stem)]

    # Month Pillar
    m_stem = STEMS[(month + 2) % 10]
    m_branch = BRANCHES[(month + 1) % 12]

    # Hour Pillar
    h_branch = BRANCHES[(hour + 1) // 2 % 12]
    h_stem = STEMS[((d_offset % 5) * 2 + (hour + 1) // 2) % 10]

    natal_pillars = {
        "year": f"{y_stem} {y_branch} ({ANIMALS[BRANCHES.index(y_branch)]})",
        "month": f"{m_stem} {m_branch} ({ANIMALS[BRANCHES.index(m_branch)]})",
        "day": f"{d_stem} {d_branch} ({ANIMALS[BRANCHES.index(d_branch)]})",
        "hour": f"{h_stem} {h_branch} ({ANIMALS[BRANCHES.index(h_branch)]})"
    }

    # 2. ACTIVE TRANSIT BAZI (Annual Pillar for target_year)
    t_y_offset = (target_year - 1984) % 60
    t_y_stem = STEMS[t_y_offset % 10]
    t_y_branch = BRANCHES[t_y_offset % 12]

    annual_transit_pillar = f"{t_y_stem} {t_y_branch} ({ANIMALS[BRANCHES.index(t_y_branch)]})"

    # 10-Year Luck Pillar phase (Da Yun approx)
    age = target_year - year
    luck_cycle_num = (age // 10) + 1
    luck_stem = STEMS[(STEMS.index(m_stem) + luck_cycle_num) % 10]
    luck_branch = BRANCHES[(BRANCHES.index(m_branch) + luck_cycle_num) % 12]
    luck_pillar = f"{luck_stem} {luck_branch} (Luck Decade #{luck_cycle_num}, Age {luck_cycle_num*10-10}-{luck_cycle_num*10-1})"

    return {
        "Year": {"Stem": y_stem, "Branch": y_branch, "Animal": ANIMALS[BRANCHES.index(y_branch)]},
        "Month": {"Stem": m_stem, "Branch": m_branch, "Animal": ANIMALS[BRANCHES.index(m_branch)]},
        "Day": {"Stem": d_stem, "Branch": d_branch, "Animal": ANIMALS[BRANCHES.index(d_branch)]},
        "Hour": {"Stem": h_stem, "Branch": h_branch, "Animal": ANIMALS[BRANCHES.index(h_branch)]},
        "DayMaster": day_master,
        "day_master": f"{d_stem} ({element})",
        "Element": element,
        "self_element": element,
        "structure": "Balanced Five-Element Cycle",
        "natal_pillars": natal_pillars,
        "pillars": natal_pillars,
        "active_transit_bazi": {
            "target_year": target_year,
            "annual_pillar": annual_transit_pillar,
            "luck_decade_pillar": luck_pillar
        }
    }
