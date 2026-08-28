# Data constants for predictions

NAK_SPAN = 360 / 27

# PRODUCTION VALIDATION STATUS (Phase 5)
DOMAIN_STATUS = {
    "Career & Authority": "PRELIMINARY VALIDATED",
    "Finance & Wealth": "PRELIMINARY VALIDATED",
    "Marriage & Relationships": "PRELIMINARY VALIDATED",
    "Health & Vitality": "INSUFFICIENT DATA",
    "Travel & Journeys": "PRELIMINARY VALIDATED",
    "Foreign Travel": "NOT TESTED"
}

HOUSE_INTERPRETATIONS = {
    1: "Focused on self, identity, and physical vitality.",
    2: "Associated with family, speech, and accumulated wealth.",
    3: "Relates to siblings, communication, courage, and short travels.",
    4: "Connected to mother, home, happiness, and real estate.",
    5: "Linked to intelligence, creativity, education, and children.",
    6: "Deals with service, health challenges, enemies, and competition.",
    7: "Represents partnerships, marriage, and public relations.",
    8: "Involved with transformation, research, longevity, and secrets.",
    9: "Relates to wisdom, higher education, long travels, and dharma.",
    10: "Connected to career, status, authority, and public reputation.",
    11: "Linked to gains, networking, goals, and elder siblings.",
    12: "Associated with isolation, spirituality, foreign lands, and liberation."
}

UPAGRAHA_INTERPRETATIONS = {
    "Gulika": "Represents karmic pressure, delays, or hidden obstacles in the house it occupies.",
    "Mandi": "Slightly less intense than Gulika, but still indicates karmic sensitivities and technical hurdles."
}

NAKSHATRA_MEANINGS = {
    "Ashwini":"New beginnings, healing, speed.",
    "Bharani":"Transformation, creativity, Yama's energy.",
    "Krittika":"Sharp, purifying, Sun's nakshatra — fame and courage.",
    "Rohini":"Growth, beauty, fertility — material pleasures.",
    "Mrigashira":"Searching, gentle, curious — good for research.",
    "Ardra":"Storms and renewal, Rudra's energy — transformation through destruction.",
    "Punarvasu":"Restoration, abundance — return of light and hope.",
    "Pushya":"Nourishment, prosperity — most auspicious nakshatra.",
    "Ashlesha":"Serpent energy, mysticism, clinging — intense.",
    "Magha":"Royal ancestors, power, authority — ancestral blessings.",
    "Purva Phalguni":"Pleasure, creativity, romance and artistic expression.",
    "Uttara Phalguni":"Patronage, contracts — good for alliances.",
    "Hasta":"Skill, dexterity, craftsmanship — healing and work.",
    "Chitra":"Brilliance, artistry — creativity and architecture.",
    "Swati":"Independence, trade — business and travel favored.",
    "Vishakha":"Goal-oriented — achievement through effort.",
    "Anuradha":"Devotion, friendship, loyalty and cooperation.",
    "Jyeshtha":"Power, seniority, Indra — leadership but watch arrogance.",
    "Mula":"Root destruction — uprooting for new growth.",
    "Purva Ashadha":"Victory, purification — early wins and optimism.",
    "Uttara Ashadha":"Final victory — lasting achievements.",
    "Shravana":"Listening, learning, Vishnu — knowledge and fame.",
    "Dhanishtha":"Wealth, music, abundance.",
    "Shatabhisha":"Healing, mystery, Varuna — medicine and secrets.",
    "Purva Bhadrapada":"Fiery transformation — intensity and wisdom.",
    "Uttara Bhadrapada":"Depth, wisdom, spiritual maturity.",
    "Revati":"Safe journey, compassion — completion and nourishment.",
}

TRANSIT_NAKSHATRA_WARNINGS = {
    "Ardra":    ("warning", "Storms and turmoil possible. Be patient."),
    "Ashlesha": ("warning", "Deception and hidden enemies. Trust carefully."),
    "Jyeshtha": ("warning", "Power struggles and ego clashes. Stay humble."),
    "Mula":     ("danger",  "Uprooting energy — unexpected losses or changes."),
    "Purva Bhadrapada": ("warning", "Intense fiery period. Control anger."),
    "Vishakha": ("caution", "Goal-driven but beware obsession and rivalry."),
    "Atiganda": ("caution", "Obstacles in path. Slow down and re-evaluate."),
    "Ganda":    ("caution", "Rough period — avoid major decisions."),
    "Vyatipata":("danger",  "Highly inauspicious yoga. Avoid new ventures."),
}
