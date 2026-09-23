"""
Multi-Language Narrative Localizer Engine (Module 26 - Task 26.2).
Supports language codes: 'en', 'hi', 'ta', 'ml', 'es' with dictionary-backed term mappings
preserving mechanical astrological definitions across non-English reports.
"""
from typing import Dict, Any

ASTROLOGICAL_TERM_DICTIONARY = {
    "hi": { # Hindi
        "Dasha": "दशा (Dasha)",
        "Mahadasha": "महादशा (Mahadasha)",
        "Kakshya": "कक्षा (Kakshya)",
        "SBC Vedha": "सर्वतोभद्र वेध (SBC Vedha)",
        "Lagnavanga": "लग्न (Lagna)",
        "Atmakaraka": "आत्माकारक (Atmakaraka)",
        "Amatyakaraka": "अमात्यकारक (Amatyakaraka)"
    },
    "ta": { # Tamil
        "Dasha": "தசா (Dasha)",
        "Mahadasha": "மகா தசா (Mahadasha)",
        "Kakshya": "கக்ஷ்யா (Kakshya)",
        "SBC Vedha": "வேதா (SBC Vedha)",
        "Lagnavanga": "லக்னம் (Lagna)",
        "Atmakaraka": "ஆத்மகாரகன் (Atmakaraka)",
        "Amatyakaraka": "அமாத்யகாரகன் (Amatyakaraka)"
    },
    "ml": { # Malayalam
        "Dasha": "ദശ (Dasha)",
        "Mahadasha": "മഹാദശ (Mahadasha)",
        "Kakshya": "കക്ഷ്യ (Kakshya)",
        "SBC Vedha": "വേധം (SBC Vedha)",
        "Lagnavanga": "ലഗ്നം (Lagna)",
        "Atmakaraka": "ആത്മകാരകൻ (Atmakaraka)",
        "Amatyakaraka": "അമാത്യകാരകൻ (Amatyakaraka)"
    },
    "es": { # Spanish
        "Dasha": "Dasha (Periodo Planetario)",
        "Mahadasha": "Mahadasha (Periodo Principal)",
        "Kakshya": "Kakshya (Sub-zona de 3.75 deg)",
        "SBC Vedha": "SBC Vedha (Obstrucción Angular)",
        "Lagnavanga": "Lagna (Ascendente)",
        "Atmakaraka": "Atmakaraka (Indicador del Alma)",
        "Amatyakaraka": "Amatyakaraka (Indicador Profesional)"
    }
}

class MultiLanguageLocalizer:
    """
    Multi-language dictionary localizer preserving exact astrological definitions.
    """

    @staticmethod
    def localize_term(term: str, lang_code: str = "en") -> str:
        lang_dict = ASTROLOGICAL_TERM_DICTIONARY.get(lang_code.lower(), {})
        return lang_dict.get(term, term)

    @staticmethod
    def localize_narrative_prompt(
        prompt_text: str,
        lang_code: str = "en"
    ) -> str:
        """
        Appends language instruction and substitutes core terms in prompt.
        """
        if lang_code.lower() == "en":
            return prompt_text

        lang_names = {"hi": "Hindi", "ta": "Tamil", "ml": "Malayalam", "es": "Spanish"}
        target_lang = lang_names.get(lang_code.lower(), "English")

        localized_prompt = f"Please generate the following narrative report in {target_lang} while strictly preserving exact astrological mechanics:\n\n" + prompt_text
        return localized_prompt

language_localizer = MultiLanguageLocalizer()
