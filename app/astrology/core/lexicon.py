VEDIC_LEXICON = {
    "Atmakaraka": "The planet with the highest degree in a sign. It represents the Soul and its primary lessons in this lifetime.",
    "Ayanamsa": "The longitudinal difference between the Tropical (Sayana) and Sidereal (Nirayana) zodiacs. Standard Jyotish uses Lahiri Ayanamsa.",
    "Bhava Chalit": "A chart showing planets according to their actual house boundaries (cusps) rather than just signs.",
    "Choghadiya": "A system of 8 auspicious and inauspicious time windows during the day and night used for selecting Muhurta.",
    "Dasha": "Planetary periods that determine when a planet will manifest its results. The most common is the 120-year Vimshottari Dasha.",
    "Dignity": "The strength or comfort level of a planet in a sign. Categories include Exalted, Moolatrikona, Own Sign, Friendly, and Debilitated.",
    "Guna Milan": "A 36-point compatibility system used for matchmaking based on the Moon's Nakshatra.",
    "KP Astrology": "Krishnamurti Paddhati. A precision system focusing on Sub-Lords and House Cusps for pinpoint event timing.",
    "Muntha": "An imaginary point in the Varshaphala (Yearly) chart that moves one sign per year from the birth Lagna. It shows the primary focus of the year.",
    "Nakshatra": "One of the 27 Lunar Mansions. Each represents a 13°20' segment of the zodiac.",
    "Panchang": "The Vedic calendar consisting of five limbs: Tithi, Vara, Nakshatra, Yoga, and Karana.",
    "Prashna": "Horary astrology. A chart calculated for the exact moment a question is asked.",
    "Raja Yoga": "A powerful combination of planets (usually Kendra and Trikona lords) indicating high status, power, and success.",
    "Sade Sati": "A 7.5-year transit of Saturn over the signs before, during, and after the natal Moon. It is a period of significant growth and challenge.",
    "Shadbala": "Six sources of planetary strength, including positional (Sthana), directional (Dig), and temporal (Kala) strength.",
    "Shodhya Pinda": "The final reduced points in Ashtakavarga after Trikona and Ekadhipatya reductions, showing the true power of a sign.",
    "Varga": "Divisional charts (like D9 Navamsa or D10 Dashamsha) used for analyzing specific areas of life like marriage or career.",
    "Vedha": "An obstruction or blockage of a transit planet's results by another planet's position.",
    "Yogini Dasha": "A secondary, 36-year dasha system often used for confirming short-term event predictions."
}

def search_lexicon(query: str):
    query = query.lower()
    return {k: v for k, v in VEDIC_LEXICON.items() if query in k.lower() or query in v.lower()}
