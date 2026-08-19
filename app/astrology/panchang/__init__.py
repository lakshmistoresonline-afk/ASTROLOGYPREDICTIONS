from datetime import date, datetime
from .tithi import get_tithi_info, get_tithi_end_time
from .nakshatra import get_nakshatra_info, get_nakshatra_end_time
from .yoga import get_yoga_info, get_yoga_end_time
from .karana import get_karana_info, get_karana_end_time
from .sky import get_sunrise, get_sunset, get_moonrise, get_moonset, get_rahu_kaal, get_gulika_kaal, get_yamaghanta
from .muhurta import get_choghadiya
from ..core.datetime import datetime_to_jd
from ..core.ephemeris import get_ayanamsa, get_planet_position
from ..core.planets import NAKSHATRA_NAMES, NAKSHATRA_LORDS
import pytz
import swisseph as swe

# Legacy names for compatibility
TITHI_NAMES = [
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
    "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
    "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi",
    "Purnima", "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
    "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
    "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi",
    "Amavasya",
]
TITHI_PAKSHA = (["Shukla"] * 15) + (["Krishna"] * 15)

YOGA_NAMES = [
    "Vishkamba", "Priti", "Ayushman", "Saubhagya", "Shobhana",
    "Atiganda", "Sukarma", "Dhriti", "Shula", "Ganda",
    "Vriddhi", "Dhruva", "Vyaghata", "Harshana", "Vajra",
    "Siddhi", "Vyatipata", "Variyan", "Parigha", "Shiva",
    "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma",
    "Indra", "Vaidhriti",
]

KARANA_NAMES = [
    "Bava", "Balava", "Kaulava", "Taitula", "Garija",
    "Vanija", "Vishti", "Shakuni", "Chatushpada", "Naga", "Kimstughna",
]

RASHI_NAMES = [
    "Mesha", "Vrishabha", "Mithuna", "Karka",
    "Simha", "Kanya", "Tula", "Vrishchika",
    "Dhanu", "Makara", "Kumbha", "Meena",
]

WEEKDAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
WEEKDAY_LORDS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]

def calculate_panchang_2_0(target_date: date, lat: float, lon: float, tz_str: str) -> dict:
    """High-precision Panchang solver."""
    tz = pytz.timezone(tz_str)
    noon_dt = datetime.combine(target_date, datetime.min.time()).replace(hour=12)
    jd_ut = datetime_to_jd(noon_dt, tz_str)

    tithi = get_tithi_info(jd_ut)
    nak = get_nakshatra_info(jd_ut)
    yoga = get_yoga_info(jd_ut)
    karana = get_karana_info(jd_ut)

    tithi_end_jd = get_tithi_end_time(jd_ut)
    nak_end_jd = get_nakshatra_end_time(jd_ut)

    def jd_to_local_str(jd):
        if jd < 0: return "—"
        y, m, d, h = swe.revjul(jd)
        hh = int(h)
        mm = int((h - hh) * 60)
        ss = int(((h - hh) * 60 - mm) * 60)
        dt_utc = datetime(y, m, d, hh, mm, ss, tzinfo=pytz.utc)
        return dt_utc.astimezone(tz).strftime("%I:%M %p")

    return {
        "tithi": {
            "number": tithi["number"],
            "end_time": jd_to_local_str(tithi_end_jd)
        },
        "nakshatra": {
            "number": nak["number"],
            "end_time": jd_to_local_str(nak_end_jd),
            "pada": nak["pada"]
        },
        "yoga": {
            "number": yoga["number"]
        },
        "karana": {
            "number": karana["number"]
        },
        "ayanamsa": round(get_ayanamsa(jd_ut), 4)
    }

def calculate_panchang(target_date: date, lat: float, lon: float, tz_str: str,
                        birth_nak_idx: int = None) -> dict:
    """Legacy compatibility wrapper for high-precision Panchang."""
    tz = pytz.timezone(tz_str)
    noon_dt = datetime.combine(target_date, datetime.min.time()).replace(hour=12)
    jd_ut = datetime_to_jd(noon_dt, tz_str)

    tithi = get_tithi_info(jd_ut)
    nak = get_nakshatra_info(jd_ut)
    yoga = get_yoga_info(jd_ut)
    karana = get_karana_info(jd_ut)

    sun_pos = get_planet_position(jd_ut, swe.SUN)
    moon_pos = get_planet_position(jd_ut, swe.MOON)

    # 1. Vara
    weekday_idx = target_date.weekday()
    indian_day_idx = (weekday_idx + 1) % 7

    # 2. Sky
    sunrise_jd = get_sunrise(jd_ut, lat, lon)
    sunset_jd = get_sunset(jd_ut, lat, lon)
    moonrise_jd = get_moonrise(jd_ut, lat, lon)
    moonset_jd = get_moonset(jd_ut, lat, lon)

    def jd_to_local_str(jd):
        if not jd or jd < 0: return "—"
        y, m, d, h = swe.revjul(jd)
        hh = int(h)
        mm = int((h - hh) * 60)
        dt_utc = datetime(y, m, d, hh, mm, tzinfo=pytz.utc)
        return dt_utc.astimezone(tz).strftime("%I:%M %p")

    def jd_to_diff_hours(jd_target):
        if not jd_target or jd_target < 0: return 0.0
        return round((jd_target - jd_ut) * 24, 1)

    tithi_idx = (tithi["number"] - 1) % 30
    yoga_idx = (yoga["number"] - 1) % 27

    tithi_nature = "Auspicious" if tithi_idx in [1, 2, 4, 6, 9, 10, 12, 14] else "Mixed"
    yoga_nature = "Auspicious" if yoga_idx in [1, 2, 3, 4, 6, 7, 10, 11, 13, 15, 17, 19, 20, 21, 22, 23, 24, 25] else "Inauspicious"

    res = {
        "date": target_date.strftime("%A, %d %B %Y"),
        "date_iso": target_date.isoformat(),
        "ayanamsa": round(get_ayanamsa(jd_ut), 4),
        "vara": {
            "name": WEEKDAYS[indian_day_idx],
            "lord": WEEKDAY_LORDS[indian_day_idx]
        },
        "tithi": {
            "number": tithi["number"],
            "name": TITHI_NAMES[tithi_idx],
            "paksha": TITHI_PAKSHA[tithi_idx],
            "nature": tithi_nature,
            "hours_remaining": jd_to_diff_hours(get_tithi_end_time(jd_ut)),
            "is_ekadashi": tithi["number"] in [11, 26],
            "is_purnima": tithi["number"] == 15,
            "is_amavasya": tithi["number"] == 30,
        },
        "nakshatra": {
            "number": nak["number"],
            "name": NAKSHATRA_NAMES[nak["number"]-1],
            "lord": NAKSHATRA_LORDS[nak["number"]-1],
            "nature": "Auspicious" if nak["number"] in [1, 4, 8, 12, 13, 15, 17, 21, 22, 26, 27] else "Mixed",
            "pada": nak["pada"],
            "hours_remaining": jd_to_diff_hours(get_nakshatra_end_time(jd_ut)),
        },
        "yoga": {
            "name": YOGA_NAMES[yoga_idx],
            "nature": yoga_nature,
            "fraction_elapsed": round(yoga["fraction"] * 100, 1)
        },
        "karana": {
            "name": KARANA_NAMES[(karana["number"]-1) % 11],
            "nature": "Neutral",
            "is_vishti": (karana["number"] % 7) == 0 # Simplified
        },
        "sun_rashi": {
            "name": RASHI_NAMES[int(sun_pos["longitude"] / 30)],
            "degree": round(sun_pos["longitude"] % 30, 2)
        },
        "moon_rashi": {
            "name": RASHI_NAMES[int(moon_pos["longitude"] / 30)],
            "degree": round(moon_pos["longitude"] % 30, 2)
        },
        "sky": {
            "sunrise": jd_to_local_str(sunrise_jd),
            "sunset": jd_to_local_str(sunset_jd),
            "moonrise": jd_to_local_str(moonrise_jd),
            "moonset": jd_to_local_str(moonset_jd),
            "solar_noon": "—", # To be implemented
            "day_length": "—", # To be implemented
            "moon_phase_name": "—", # To be implemented
            "moon_phase_pct": 0,
            "rahu_kaal": get_rahu_kaal(weekday_idx, sunrise_jd or 0, sunset_jd or 0),
            "gulika_kaal": get_gulika_kaal(weekday_idx, sunrise_jd or 0, sunset_jd or 0),
            "yamaghanta": get_yamaghanta(weekday_idx, sunrise_jd or 0, sunset_jd or 0),
        },
        "is_auspicious": tithi_nature == "Auspicious" and yoga_nature == "Auspicious",
        "choghadiya": [],
        "muhurtas": {}
    }

    # 3. Precision Muhurtas
    from .muhurta import get_abhijit_muhurta, get_brahma_muhurta, get_amrit_kaal
    if sunrise_jd and sunset_jd:
        # Abhijit
        ab_s, ab_e = get_abhijit_muhurta(sunrise_jd, sunset_jd)
        res["muhurtas"]["Abhijit"] = f"{jd_to_local_str(ab_s)} – {jd_to_local_str(ab_e)}"
        res["abhijit_muhurta"] = res["muhurtas"]["Abhijit"] # Legacy compatibility

        # Brahma
        br_s, br_e = get_brahma_muhurta(sunrise_jd, sunset_jd)
        res["muhurtas"]["Brahma"] = f"{jd_to_local_str(br_s)} – {jd_to_local_str(br_e)}"

        # Amrit Kaal
        nak_start = jd_ut # Approximate start for current day if not known
        nak_end = get_nakshatra_end_time(jd_ut)
        am_kaal = get_amrit_kaal(nak["number"], nak_start, nak_end)
        if am_kaal:
            res["muhurtas"]["Amrit Kaal"] = f"{jd_to_local_str(am_kaal[0])} – {jd_to_local_str(am_kaal[1])}"
        else:
            res["muhurtas"]["Amrit Kaal"] = "—"

    # 4. Choghadiya
    if sunrise_jd and sunset_jd:
        # Approximate next sunrise
        next_sr = get_sunrise(jd_ut + 1.0, lat, lon) or (sunrise_jd + 1.0)
        ch_raw = get_choghadiya(sunrise_jd, sunset_jd, next_sr, indian_day_idx)
        for c in ch_raw:
            res["choghadiya"].append({
                "name": c["name"],
                "start": jd_to_local_str(c["start_jd"]),
                "end": jd_to_local_str(c["end_jd"]),
                "type": c["type"]
            })

    # Tarabala / Chandra Bala
    if birth_nak_idx is not None:
        from .utils import calculate_tarabala, calculate_chandra_bala
        res["tarabala"] = calculate_tarabala(nak["number"]-1, birth_nak_idx)
        moon_rashi = int(moon_pos["longitude"] / 30)
        # Legacy passed birth_nak_idx as rashi in some paths. This is still a bit broken but better.
        res["chandra_bala"] = calculate_chandra_bala(moon_rashi, int(birth_nak_idx / 2.25))

    return res
