from typing import Dict, List, Any

# Stems and Branches
STEMS = ["Jia", "Yi", "Bing", "Ding", "Wu", "Ji", "Geng", "Xin", "Ren", "Gui"]
BRANCHES = ["Zi", "Chou", "Yin", "Mao", "Chen", "Si", "Wu", "Wei", "Shen", "You", "Xu", "Hai"]
ANIMALS = ["Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake", "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig"]
ELEMENTS = ["Wood", "Wood", "Fire", "Fire", "Earth", "Earth", "Metal", "Metal", "Water", "Water"]

def calculate_bazi_pillars(year: int, month: int, day: int, hour: int) -> Dict[str, Any]:
    """
    Four Pillars of Destiny (Bazi) calculation.
    Uses basic year-start and day-count offsets.
    """
    # 1. Year Pillar
    # Year 1984 was Wood Rat (Jia Zi)
    year_offset = (year - 1984) % 60
    y_stem = STEMS[year_offset % 10]
    y_branch = BRANCHES[year_offset % 12]

    # 2. Day Pillar (Simplified JDN calculation)
    # Ref point: 2000-01-01 was Metal Dragon (Geng Chen)
    from datetime import date
    d1 = date(2000, 1, 1)
    d2 = date(year, month, day)
    days_diff = (d2 - d1).days

    day_offset = (days_diff + 16) % 60 # 16 is offset for Geng Chen
    d_stem = STEMS[day_offset % 10]
    d_branch = BRANCHES[day_offset % 12]

    # Day Master is the Day Stem
    day_master = d_stem

    # 3. Month Pillar (Based on Solar Terms - Placeholder)
    m_stem = STEMS[(month + 2) % 10]
    m_branch = BRANCHES[(month + 1) % 12]

    # 4. Hour Pillar
    h_branch = BRANCHES[(hour + 1) // 2 % 12]
    h_stem = STEMS[((day_offset % 5) * 2 + (hour + 1) // 2) % 10]

    return {
        "Year": {"Stem": y_stem, "Branch": y_branch, "Animal": ANIMALS[BRANCHES.index(y_branch)]},
        "Month": {"Stem": m_stem, "Branch": m_branch, "Animal": ANIMALS[BRANCHES.index(m_branch)]},
        "Day": {"Stem": d_stem, "Branch": d_branch, "Animal": ANIMALS[BRANCHES.index(d_branch)]},
        "Hour": {"Stem": h_stem, "Branch": h_branch, "Animal": ANIMALS[BRANCHES.index(h_branch)]},
        "DayMaster": day_master,
        "Element": ELEMENTS[STEMS.index(d_stem)]
    }
