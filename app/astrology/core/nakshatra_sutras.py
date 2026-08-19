NAKSHATRA_SUTRAS = {
    "Ashwini": "Speed of thought and healing touch; beginnings are blessed with vitality.",
    "Bharani": "The fire of restraint; transformative results through intense focus.",
    "Krittika": "Sharp intellect and purification; cutting through obstacles with logic.",
    "Rohini": "Growth and creative magnetism; attraction of material and aesthetic wealth.",
    "Mrigashira": "The searching soul; discovery through curiosity and gentle persistence.",
    "Ardra": "Storm of transformation; renewal through the release of old patterns.",
    "Punarvasu": "Return of the light; abundance through harmony and restoration.",
    "Pushya": "Divine nourishment; the most auspicious foundation for spiritual growth.",
    "Ashlesha": "Intense mystical perception; power through deep intuitive understanding.",
    "Magha": "Ancestral authority; leadership fueled by tradition and duty.",
    "Purva Phalguni": "Creative enjoyment; success through relaxation and social charm.",
    "Uttara Phalguni": "The power of alliance; stability through contracts and commitment.",
    "Hasta": "Manifestation through skill; results gained by the labor of one's own hands.",
    "Chitra": "Brilliant architecture; beauty through structured and detailed design.",
    "Swati": "Independent movement; success in trade and individual expression.",
    "Vishakha": "Focused ambition; achievement through single-minded determination.",
    "Anuradha": "Devotion and cooperation; victory through friendship and loyalty.",
    "Jyeshtha": "Supreme seniority; wisdom gained through inner mastery and power.",
    "Mula": "Root destruction; reaching the core truth by uprooting illusions.",
    "Purva Ashadha": "Early victory; purification leading to optimistic success.",
    "Uttara Ashadha": "Enduring achievement; lasting legacy through perseverance.",
    "Shravana": "Deep listening; knowledge gained through receptivity and silence.",
    "Dhanishtha": "Rhythmic abundance; wealth through musical or social harmony.",
    "Shatabhisha": "100 healers; mystery and secrets leading to profound healing.",
    "Purva Bhadrapada": "Idealistic transformation; intense devotion to a higher cause.",
    "Uttara Bhadrapada": "Spiritual maturity; depth of wisdom and oceanic calm.",
    "Revati": "Final nourishment; safe passage and completion of the journey."
}

def get_nakshatra_sutra(nak_name: str) -> str:
    return NAKSHATRA_SUTRAS.get(nak_name, "Celestial influence on the path.")
