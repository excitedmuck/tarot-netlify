"""SEO meta tags, structured data, and Open Graph for Mystical Tarot de Multiverse."""

SITE_URL = "https://mystical-tarot.netlify.app"
SITE_NAME = "Mystical Tarot de Multiverse"
SITE_DESCRIPTION = (
    "Free tarot card readings, numerology life path calculator, I Ching hexagram oracle, "
    "and AI-powered cosmic insights. Discover your soul's blueprint through the ancient arts."
)
SITE_KEYWORDS = (
    "free tarot reading, tarot cards online, numerology calculator, life path number, "
    "I Ching oracle, hexagram reading, celtic cross tarot, three card spread, "
    "ai tarot, cosmic reading, soul urge number, expression number, master numbers, "
    "free psychic reading, daily tarot, tarot interpretation, numerology free"
)
TWITTER_HANDLE = "@cacooleed"


def get_meta_html(
    title: str = None,
    description: str = None,
    page_type: str = "website",
    canonical: str = None,
) -> str:
    """Return HTML string with all SEO meta tags to inject via st.markdown."""
    t = title or SITE_NAME
    d = description or SITE_DESCRIPTION
    url = canonical or SITE_URL

    return f"""
<head>
<!-- Primary SEO -->
<title>{t}</title>
<meta name="description" content="{d}" />
<meta name="keywords" content="{SITE_KEYWORDS}" />
<meta name="robots" content="index, follow" />
<meta name="author" content="Mystical Tarot de Multiverse" />
<link rel="canonical" href="{url}" />

<!-- Open Graph / Facebook -->
<meta property="og:type" content="{page_type}" />
<meta property="og:url" content="{url}" />
<meta property="og:title" content="{t}" />
<meta property="og:description" content="{d}" />
<meta property="og:site_name" content="{SITE_NAME}" />
<meta property="og:image" content="{SITE_URL}/og-image.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:site" content="{TWITTER_HANDLE}" />
<meta name="twitter:title" content="{t}" />
<meta name="twitter:description" content="{d}" />
<meta name="twitter:image" content="{SITE_URL}/og-image.png" />

<!-- Structured Data: WebApplication -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "{SITE_NAME}",
  "url": "{SITE_URL}",
  "description": "{SITE_DESCRIPTION}",
  "applicationCategory": "LifestyleApplication",
  "operatingSystem": "Web",
  "offers": {{
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD"
  }},
  "keywords": "tarot, numerology, I Ching, oracle, cosmic readings",
  "author": {{
    "@type": "Person",
    "name": "Mystical Tarot de Multiverse",
    "url": "https://twitter.com/cacooleed"
  }},
  "featureList": [
    "Free tarot card readings",
    "Numerology life path calculator",
    "I Ching hexagram oracle",
    "AI-powered cosmic interpretations",
    "Personal reading journal",
    "Celtic Cross, Three-Card, and Elemental spreads"
  ]
}}
</script>

<!-- FAQ Schema for SEO rich snippets -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {{
      "@type": "Question",
      "name": "What is a tarot card reading?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "A tarot card reading uses a deck of 78 cards to explore your past, present, and possible future. Each card carries archetypal imagery that can illuminate your situation and inner landscape."
      }}
    }},
    {{
      "@type": "Question",
      "name": "How is a life path number calculated?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "Your life path number is calculated by reducing your full birth date (month + day + year) to a single digit or master number (11, 22, or 33) using the Pythagorean method."
      }}
    }},
    {{
      "@type": "Question",
      "name": "What is the I Ching?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "The I Ching (Book of Changes) is an ancient Chinese oracle with 64 hexagrams. Each hexagram offers wisdom about your situation through the interplay of yin and yang energies, guiding decision-making and reflection."
      }}
    }},
    {{
      "@type": "Question",
      "name": "Is this tarot reading free?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "Yes! All readings — tarot, numerology, and I Ching — are completely free. Sign in with Google to save your readings and unlock AI-powered pattern insights from your personal journal."
      }}
    }}
  ]
}}
</script>
</head>
"""


# Marketing copy for A/B testing variants
AB_VARIANTS = {
    "A": {
        "hero_headline": "Mystical Tarot de Multiverse",
        "hero_subtitle": "Free Tarot · Numerology · Cosmic Readings",
        "hero_tagline": "The cards are a mirror held up to the soul — not a cage, but a lantern. Breathe. Ask what stirs inside you, and let the cosmos answer.",
        "tarot_cta": "Unveil the {spread}",
        "numerology_cta": "Reveal My Numbers",
        "iching_cta": "Cast the Hexagram",
        "journal_prompt": "Sign in with Google to save your readings, track your journey, and receive personalised AI insights over time.",
    },
    "B": {
        "hero_headline": "Your Free Cosmic Reading",
        "hero_subtitle": "Tarot · Numerology · I Ching · AI Insights",
        "hero_tagline": "Discover the patterns shaping your life. Ask a question, draw your cards, and let ancient wisdom meet modern AI to illuminate your path.",
        "tarot_cta": "Draw My {spread} Cards",
        "numerology_cta": "Calculate My Life Path",
        "iching_cta": "Consult the I Ching",
        "journal_prompt": "Create a free account to save all your readings and discover AI-detected patterns in your cosmic journey over time.",
    },
}
