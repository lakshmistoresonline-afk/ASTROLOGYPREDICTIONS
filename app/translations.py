TRANSLATIONS = {
    "en": {
        "nav_home": "Home",
        "nav_matchmaking": "Matchmaking",
        "nav_predictions": "Daily Predictions",
        "nav_transit": "Transit Chart",
        "nav_dasha": "Dasha Periods",
        "nav_panchang": "Panchang",
        "nav_prashna": "Prashna",
        "nav_yearly": "Yearly Chart",
        "chart_title": "Kundli Chart",
        "lagna": "Lagna",
        "rashi": "Rashi",
        "nakshatra": "Nakshatra",
        "dignity": "Dignity",
        "strength": "Planetary Strength",
        "remedies": "Remedies",
        "download_pdf": "PDF",
        "save_chart": "Save Chart"
    },
    "hi": {
        "nav_home": "मुखपृष्ठ",
        "nav_matchmaking": "मिलान",
        "nav_predictions": "दैनिक भविष्यफल",
        "nav_transit": "गोचर कुंडली",
        "nav_dasha": "दशा चक्र",
        "nav_panchang": "पंचांग",
        "nav_prashna": "प्रश्न कुंडली",
        "nav_yearly": "वर्षफल",
        "chart_title": "जन्म कुंडली",
        "lagna": "लग्न",
        "rashi": "राशि",
        "nakshatra": "नक्षत्र",
        "dignity": "स्थिति",
        "strength": "ग्रह बल",
        "remedies": "उपाय",
        "download_pdf": "पीडीएफ",
        "save_chart": "सुरक्षित करें"
    }
}

def translate(key: str, lang: str = "en") -> str:
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)
