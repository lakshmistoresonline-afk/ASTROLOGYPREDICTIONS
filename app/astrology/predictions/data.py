# Data constants for predictions

NAK_SPAN = 360 / 27

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
