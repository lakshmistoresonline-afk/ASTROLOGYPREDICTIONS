import os

seo_pages = [
    'vedic-astrology', 'birth-chart', 'kundli', 'dasha', 'transits',
    'career-astrology', 'marriage-astrology', 'finance-astrology',
    'business-astrology', 'property-astrology', 'education-astrology',
    'children-astrology', 'foreign-settlement-astrology', 'spirituality-astrology', 'life-timeline'
]

articles = [
    'what-is-a-vedic-birth-chart', 'what-is-a-lagna', 'what-is-a-nakshatra',
    'what-is-vimshottari-dasha', 'what-are-planetary-transits', 'how-is-a-vedic-horoscope-calculated',
    'why-exact-birth-time-matters', 'why-birth-location-matters', 'what-is-a-d10-chart', 'what-is-a-d9-chart',
    'what-is-a-life-atlas', 'how-career-timing-is-interpreted'
]

os.makedirs('app/templates/marketing/seo', exist_ok=True)
os.makedirs('app/templates/marketing/articles', exist_ok=True)

for p in seo_pages:
    path = f'app/templates/marketing/seo/{p}.html'
    title = p.replace('-', ' ').title()
    content = f'''{{% extends "marketing/seo_base.html" %}}
{{% block content %}}
<h1>{title}</h1>
<p class="lead text-muted">Explore {title.lower()} through precision Vedic astrology intelligence, deterministic astronomical calculations, and exact chart analysis.</p>
<hr class="my-4 border-secondary">
<h3>Understanding {title}</h3>
<p>Astro Predictions brings deterministic calculation and authentic Vedic astrology interpretation to your personal chart. Go beyond generic daily horoscopes with chart-based insights.</p>
{{% endblock %}}
'''
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

for a in articles:
    path = f'app/templates/marketing/articles/{a}.html'
    title = a.replace('-', ' ').title()
    content = f'''{{% extends "marketing/seo_base.html" %}}
{{% block content %}}
<h1>{title}</h1>
<p class="lead text-muted">Educational insights into {title.lower()} within Vedic astrology.</p>
<hr class="my-4 border-secondary">
<p>Detailed educational guide on {title.lower()}, explaining foundational principles of Vedic astrology and astronomical calculation.</p>
{{% endblock %}}
'''
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

# Learn hub template
with open('app/templates/marketing/learn.html', 'w', encoding='utf-8') as f:
    f.write('''{% extends "marketing/seo_base.html" %}
{% block content %}
<h1>Astro Predictions Learning Hub</h1>
<p class="lead text-muted">Master Vedic astrology principles, chart calculations, and timing systems.</p>
<hr class="my-4 border-secondary">
<div class="list-group">
{% for art in articles %}
<a href="/learn/{{ art }}" class="list-group-item list-group-item-action bg-dark text-warning border-secondary mb-2 rounded">{{ art.replace('-', ' ').title() }}</a>
{% endfor %}
</div>
{% endblock %}
''')

# Privacy
with open('app/templates/marketing/privacy.html', 'w', encoding='utf-8') as f:
    f.write('''{% extends "marketing/seo_base.html" %}
{% block content %}
<h1>Privacy Policy</h1>
<p>Your birth details are treated with strict confidentiality. We store birth data solely to compute your astrological charts and predictions. We never sell personal data.</p>
{% endblock %}
''')

# Terms
with open('app/templates/marketing/terms.html', 'w', encoding='utf-8') as f:
    f.write('''{% extends "marketing/seo_base.html" %}
{% block content %}
<h1>Terms of Service</h1>
<p>Astro Predictions provides Vedic astrology interpretations for informational and personal reflection purposes only. Not professional medical, legal, or financial advice.</p>
{% endblock %}
''')

# About
with open('app/templates/marketing/about.html', 'w', encoding='utf-8') as f:
    f.write('''{% extends "marketing/seo_base.html" %}
{% block content %}
<h1>About Astro Predictions</h1>
<p>Astro Predictions combines precise astronomical calculation engines with authentic Vedic astrology to deliver personal intelligence without generic horoscopes.</p>
{% endblock %}
''')

# Contact
with open('app/templates/marketing/contact.html', 'w', encoding='utf-8') as f:
    f.write('''{% extends "marketing/seo_base.html" %}
{% block content %}
<h1>Contact Us</h1>
<p>Reach out to the Astro Predictions team at support@astropredictions.app.</p>
{% endblock %}
''')

print('Successfully generated marketing templates.')
