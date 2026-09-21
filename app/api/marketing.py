from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, Response, send_from_directory
import os
import json
import uuid
from datetime import datetime
from ..astrology.core.calculation_config import calculate_canonical_chart
from ..astrology.core.calc_client import calc_client
from ..astrology.core.datetime import parse_birth_datetime

marketing_bp = Blueprint("marketing", __name__)

PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL", "https://astropredictions.app")
ANDROID_STORE_URL = os.getenv("ANDROID_STORE_URL", "https://play.google.com/store/apps/details?id=com.trademind.astrology")

SEO_PAGES = [
    "vedic-astrology", "birth-chart", "kundli", "dasha", "transits",
    "career-astrology", "marriage-astrology", "finance-astrology",
    "business-astrology", "property-astrology", "education-astrology",
    "children-astrology", "foreign-settlement-astrology", "spirituality-astrology", "life-timeline"
]

LEARN_ARTICLES = [
    "what-is-a-vedic-birth-chart", "what-is-a-lagna", "what-is-a-nakshatra",
    "what-is-vimshottari-dasha", "what-are-planetary-transits", "how-is-a-vedic-horoscope-calculated",
    "why-exact-birth-time-matters", "why-birth-location-matters", "what-is-a-d10-chart", "what-is-a-d9-chart",
    "what-is-a-life-atlas", "how-career-timing-is-interpreted"
]

@marketing_bp.before_request
def capture_attribution():
    utm_source = request.args.get("utm_source")
    utm_medium = request.args.get("utm_medium")
    utm_campaign = request.args.get("utm_campaign")
    utm_content = request.args.get("utm_content")
    utm_term = request.args.get("utm_term")
    ref = request.args.get("ref") or request.args.get("referral_code")

    if utm_source or utm_medium or ref:
        session["attribution"] = {
            "source": utm_source or "direct",
            "medium": utm_medium or "none",
            "campaign": utm_campaign or "none",
            "content": utm_content or "",
            "term": utm_term or "",
            "referral": ref or "",
            "timestamp": datetime.utcnow().isoformat()
        }

@marketing_bp.route("/")
@marketing_bp.route("/welcome")
def home():
    return render_template("marketing/welcome.html", android_store_url=ANDROID_STORE_URL, public_base_url=PUBLIC_BASE_URL)

@marketing_bp.route("/landing")
def landing():
    return redirect(url_for("marketing.home"))

@marketing_bp.route("/download-report")
def download_commercial_report():
    return send_from_directory(os.getcwd(), "ASTRO_PREDICTIONS_COMMERCIAL_REPORT.md", as_attachment=True)

@marketing_bp.route("/birth-chart", methods=["GET", "POST"])
def birth_chart_funnel():
    preview_data = None
    error_msg = None
    if request.method == "POST":
        name = request.form.get("name", "Seeker")
        dob = request.form.get("dob")
        tob = request.form.get("tob")
        place = request.form.get("place")
        lat = request.form.get("lat")
        lon = request.form.get("lon")
        tz = request.form.get("tz")

        try:
            if not dob or not tob or not place:
                raise ValueError("Birth date, birth time, and birth place are mandatory.")

            from ..api.external import geocode_place
            if not lat or not lon or not tz:
                geo = geocode_place(place)
                if geo:
                    lat, lon, tz = geo["lat"], geo["lon"], geo["timezone"]
                else:
                    raise ValueError(f"Could not resolve precise location and timezone for '{place}'. Please provide valid birthplace.")

            dt = parse_birth_datetime(dob, tob)
            chart = calculate_canonical_chart(dt, float(lat), float(lon), str(tz))
            from ..astrology.core.houses import RASHI_NAMES
            preview_data = {
                "name": name,
                "ascendant_rashi": RASHI_NAMES[chart.asc_rashi],
                "moon_rashi": RASHI_NAMES[chart.planets["Moon"].rashi] if "Moon" in chart.planets else "N/A",
                "nakshatra": chart.planets["Moon"].nakshatra.name if "Moon" in chart.planets else "N/A",
                "dasha": "Vimshottari Dasha Active",
                "chart_fingerprint": chart.chart_fingerprint
            }
        except Exception as e:
            error_msg = f"Calculation error: {e}"

    return render_template("marketing/birth_chart.html", preview_data=preview_data, error_msg=error_msg, android_store_url=ANDROID_STORE_URL)

@marketing_bp.route("/share/<token>")
def share_card(token):
    share_info = {
        "title": "Astro Predictions — Vedic Astrology Intelligence",
        "description": "Explore personalized Vedic birth chart, transits, and Dasha timing.",
        "image": f"{PUBLIC_BASE_URL}/static/img/og-default.png",
        "url": f"{PUBLIC_BASE_URL}/share/{token}"
    }
    return render_template("marketing/share.html", share=share_info, android_store_url=ANDROID_STORE_URL)

@marketing_bp.route("/r/<code_str>")
def referral(code_str):
    session["referral_code"] = code_str
    return redirect(url_for("marketing.home"))

@marketing_bp.route("/download")
def download():
    return render_template("marketing/download.html", android_store_url=ANDROID_STORE_URL)

@marketing_bp.route("/learn")
def learn():
    return render_template("marketing/learn.html", articles=LEARN_ARTICLES)

@marketing_bp.route("/learn/<article_slug>")
def learn_article(article_slug):
    if article_slug not in LEARN_ARTICLES:
        return "Article not found", 404
    return render_template(f"marketing/articles/{article_slug}.html", slug=article_slug)

@marketing_bp.route("/privacy")
def privacy():
    return render_template("marketing/privacy.html")

@marketing_bp.route("/terms")
def terms():
    return render_template("marketing/terms.html")

@marketing_bp.route("/refund-policy")
def refund_policy():
    return render_template("marketing/refund_policy.html")

@marketing_bp.route("/subscription-policy")
def subscription_policy():
    return render_template("marketing/subscription_policy.html")

@marketing_bp.route("/about")
def about():
    return render_template("marketing/about.html")

@marketing_bp.route("/contact")
def contact():
    return render_template("marketing/contact.html")

for page in SEO_PAGES:
    def make_seo_route(p):
        @marketing_bp.route(f"/{p}")
        def seo_page():
            return render_template(f"marketing/seo/{p}.html", page_slug=p, android_store_url=ANDROID_STORE_URL, public_base_url=PUBLIC_BASE_URL)
        seo_page.__name__ = f"seo_{p.replace('-', '_')}"
        return seo_page
    marketing_bp.add_url_rule(f"/{page}", f"seo_{page.replace('-', '_')}", make_seo_route(page))

@marketing_bp.route("/robots.txt")
def robots_txt():
    content = f"""User-agent: *
Allow: /
Allow: /welcome
Allow: /birth-chart
Allow: /learn
Allow: /download
Allow: /download-report
Allow: /privacy
Allow: /terms
Allow: /refund-policy
Allow: /subscription-policy
Allow: /about
Allow: /contact
"""
    for p in SEO_PAGES:
        content += f"Allow: /{p}\n"
    content += f"Sitemap: {PUBLIC_BASE_URL}/sitemap.xml\n"
    return Response(content, mimetype="text/plain")

@marketing_bp.route("/sitemap.xml")
def sitemap_xml():
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    urls = ["/", "/welcome", "/birth-chart", "/download", "/download-report", "/learn", "/privacy", "/terms", "/refund-policy", "/subscription-policy", "/about", "/contact"]
    for p in SEO_PAGES:
        urls.append(f"/{p}")
    for a in LEARN_ARTICLES:
        urls.append(f"/learn/{a}")

    for u in urls:
        xml.append("  <url>")
        xml.append(f"    <loc>{PUBLIC_BASE_URL}{u}</loc>")
        xml.append(f"    <lastmod>{datetime.utcnow().strftime('%Y-%m-%d')}</lastmod>")
        xml.append("    <changefreq>weekly</changefreq>")
        xml.append("    <priority>0.8</priority>")
        xml.append("  </url>")

    xml.append('</urlset>')
    return Response("\n".join(xml), mimetype="application/xml")
