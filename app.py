import streamlit as st
import random
import openai
from datetime import datetime
import os
import hashlib
import math

st.set_page_config(
    page_title="Mystical Tarot de Multiverse | Free Tarot & Numerology Readings",
    page_icon="🔮",
    layout="wide"
)

openai.api_key = os.getenv("OPENAI_API_KEY")

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700&family=Crimson+Pro:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Space+Grotesk:wght@300;400;500&display=swap');

:root {
    --bg:       #0c1520;
    --bg2:      #12203a;
    --bg3:      #182d4a;
    --gold:     #c9a96e;
    --gold-l:   #e8c98e;
    --arctic:   #7ec4cc;
    --lavender: #b89ec4;
    --parchment:#e8dcc8;
    --sage:     #8aaa7c;
    --terra:    #c47a5a;
    --slate:    #2d4a5a;
    --muted:    #6a8a9a;
    --border:   rgba(201,169,110,0.18);
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    color: var(--parchment) !important;
    font-family: 'Crimson Pro', Georgia, serif !important;
}
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 60% 40% at 15% 5%, rgba(126,196,204,0.07) 0%, transparent 100%),
        radial-gradient(ellipse 50% 60% at 85% 95%, rgba(184,158,196,0.09) 0%, transparent 100%),
        var(--bg) !important;
}
.main .block-container {
    padding: 2rem 3rem 4rem !important;
    max-width: 1280px !important;
    margin: 0 auto !important;
}
[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #080f1a 0%, #0c1520 60%, #10182a 100%) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] label { color: var(--parchment) !important; }
[data-testid="stSidebar"] a { color: var(--gold) !important; text-decoration: none !important; }
[data-testid="stSidebar"] a:hover { color: var(--gold-l) !important; text-decoration: underline !important; }
[data-testid="stSidebar"] h2 { color: var(--arctic) !important; font-family: 'Cinzel Decorative', serif !important; font-size: 0.9rem !important; letter-spacing: 0.06em; }

h1, h2, h3, h4 { font-family: 'Cinzel Decorative', 'Times New Roman', serif !important; letter-spacing: 0.04em !important; }
h1 {
    color: var(--gold) !important;
    font-size: clamp(1.3rem, 3vw, 2.2rem) !important;
    text-shadow: 0 0 40px rgba(201,169,110,0.35), 0 0 80px rgba(201,169,110,0.1) !important;
    line-height: 1.35 !important;
}
h2 { color: var(--arctic) !important; font-size: clamp(0.95rem, 2vw, 1.35rem) !important; }
h3 { color: var(--lavender) !important; font-size: 1rem !important; }
p, li { font-size: 1.05rem; line-height: 1.75; }

[data-testid="stTabs"] [role="tablist"] { border-bottom: 1px solid var(--border) !important; gap: 0.25rem !important; }
[data-testid="stTabs"] button {
    font-family: 'Cinzel Decorative', serif !important;
    color: var(--muted) !important;
    font-size: 0.7rem !important;
    padding: 0.65rem 1.6rem !important;
    border-radius: 4px 4px 0 0 !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    background: transparent !important;
    transition: all 0.25s ease !important;
    letter-spacing: 0.07em !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: var(--gold) !important;
    border-bottom: 2px solid var(--gold) !important;
    background: rgba(201,169,110,0.05) !important;
}
[data-testid="stTabs"] button:hover { color: var(--parchment) !important; background: rgba(255,255,255,0.03) !important; }

.stButton > button {
    background: linear-gradient(135deg, rgba(201,169,110,0.1), rgba(126,196,204,0.07)) !important;
    border: 1px solid rgba(201,169,110,0.45) !important;
    color: var(--gold) !important;
    font-family: 'Cinzel Decorative', serif !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.12em !important;
    padding: 0.7rem 2.8rem !important;
    border-radius: 3px !important;
    transition: all 0.3s ease !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, rgba(201,169,110,0.22), rgba(126,196,204,0.14)) !important;
    box-shadow: 0 0 28px rgba(201,169,110,0.18), inset 0 0 15px rgba(201,169,110,0.04) !important;
    border-color: var(--gold) !important;
    transform: translateY(-2px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

[data-baseweb="input"] input, [data-baseweb="textarea"] textarea {
    background: rgba(18,32,58,0.9) !important;
    border: 1px solid var(--slate) !important;
    color: var(--parchment) !important;
    border-radius: 4px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.95rem !important;
    transition: border-color 0.2s ease !important;
}
[data-baseweb="input"] input:focus {
    border-color: rgba(201,169,110,0.55) !important;
    box-shadow: 0 0 0 2px rgba(201,169,110,0.1) !important;
}
input::placeholder, textarea::placeholder { color: var(--muted) !important; }

[data-baseweb="select"] > div:first-child {
    background: rgba(18,32,58,0.9) !important;
    border-color: var(--slate) !important;
    color: var(--parchment) !important;
}
[data-testid="stDateInput"] input { background: rgba(18,32,58,0.9) !important; border-color: var(--slate) !important; color: var(--parchment) !important; }

[data-testid="stAlert"] {
    background: rgba(184,158,196,0.08) !important;
    border: 1px solid rgba(184,158,196,0.22) !important;
    border-radius: 6px !important;
    color: var(--lavender) !important;
    font-family: 'Crimson Pro', serif !important;
}

hr { border: none !important; border-top: 1px solid var(--border) !important; margin: 2rem 0 !important; }
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--slate); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(201,169,110,0.35); }

[data-testid="stWidgetLabel"] p {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.78rem !important;
    color: var(--muted) !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
}

/* Famous person cards */
.person-grid { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 12px; }
.person-card {
    background: linear-gradient(135deg, rgba(24,45,74,0.9), rgba(18,32,58,0.95));
    border: 1px solid rgba(201,169,110,0.2);
    border-radius: 8px;
    padding: 12px 14px;
    flex: 1 1 160px;
    max-width: 210px;
    transition: border-color 0.25s, transform 0.2s;
    text-align: center;
}
.person-card:hover { border-color: rgba(201,169,110,0.5); transform: translateY(-2px); }
.person-avatar {
    width: 48px; height: 48px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--bg3), var(--slate));
    border: 1px solid rgba(201,169,110,0.35);
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 8px;
    font-family: 'Cinzel Decorative', serif;
    font-size: 1.1rem;
    color: var(--gold);
}
.person-name { font-family: 'Space Grotesk', sans-serif; font-size: 0.78rem; font-weight: 500; color: var(--parchment); margin: 0; }
.person-desc { font-family: 'Crimson Pro', serif; font-size: 0.78rem; color: var(--muted); margin: 3px 0 6px; line-height: 1.3; }
.person-link { font-family: 'Space Grotesk', sans-serif; font-size: 0.65rem; color: var(--arctic); text-decoration: none; letter-spacing: 0.04em; text-transform: uppercase; }
.person-link:hover { color: var(--gold); }

/* Numerology number card */
.num-card {
    background: linear-gradient(160deg, rgba(24,45,74,0.95), rgba(18,32,58,1));
    border: 1px solid rgba(201,169,110,0.22);
    border-radius: 10px;
    padding: 20px 16px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.num-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
    opacity: 0.5;
}
.num-card-label { font-family: 'Space Grotesk', sans-serif; font-size: 0.68rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted); margin: 0 0 6px; }
.num-card-number { font-family: 'Cinzel Decorative', serif; font-size: 3rem; color: var(--gold); margin: 0; line-height: 1; text-shadow: 0 0 20px rgba(201,169,110,0.4); }
.num-card-title { font-family: 'Cinzel Decorative', serif; font-size: 0.72rem; color: var(--arctic); margin: 8px 0 4px; letter-spacing: 0.06em; }
.num-card-master { font-size: 0.62rem; color: var(--terra); letter-spacing: 0.08em; text-transform: uppercase; margin: 0 0 6px; }
.num-card-meaning { font-family: 'Crimson Pro', serif; font-size: 0.88rem; color: #b0c0d0; margin: 0; line-height: 1.5; }

/* Tarot card display */
.tarot-card {
    background: linear-gradient(160deg, rgba(24,45,74,0.97), rgba(14,27,46,1));
    border: 1px solid rgba(201,169,110,0.25);
    border-radius: 8px;
    padding: 14px 10px 12px;
    text-align: center;
    transition: border-color 0.25s, box-shadow 0.25s;
    margin-bottom: 8px;
}
.tarot-card:hover {
    border-color: rgba(201,169,110,0.5);
    box-shadow: 0 4px 24px rgba(201,169,110,0.1);
}
.tarot-pos { font-family: 'Space Grotesk', sans-serif; font-size: 0.62rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.07em; margin: 0 0 4px; }
.tarot-name { font-family: 'Cinzel Decorative', serif; font-size: 0.65rem; color: var(--gold); margin: 8px 0 0; line-height: 1.4; }

/* Section separator ornament */
.ornament { text-align: center; color: rgba(201,169,110,0.4); letter-spacing: 0.3em; font-size: 0.85rem; margin: 0.5rem 0; }

/* Interpretation paragraphs */
.interp-para {
    background: rgba(18,32,58,0.4);
    border-left: 2px solid rgba(201,169,110,0.3);
    border-radius: 0 6px 6px 0;
    padding: 12px 16px;
    margin-bottom: 10px;
    font-size: 1.05rem;
    line-height: 1.75;
    color: var(--parchment);
}
</style>
""", unsafe_allow_html=True)


# ── SVG utilities ─────────────────────────────────────────────────────────────

def _rng(seed_str):
    s = int(hashlib.md5(seed_str.encode()).hexdigest(), 16) % 99999
    return random.Random(s)


def header_svg() -> str:
    w, h = 1100, 90
    rng = _rng("header")
    stars = "".join(
        f'<circle cx="{rng.randint(0,w)}" cy="{rng.randint(0,h)}" r="{rng.uniform(0.4,1.8):.1f}" '
        f'fill="white" opacity="{rng.uniform(0.15,0.65):.2f}"/>'
        for _ in range(55)
    )
    arms = ""
    for i in range(8):
        a = math.radians(i * 45 - 90)
        r = 34 if i % 2 == 0 else 24
        arms += (
            f'<line x1="550" y1="45" x2="{550 + r*math.cos(a):.1f}" y2="{45 + r*math.sin(a):.1f}" '
            f'stroke="#c9a96e" stroke-width="1.4" opacity="0.65" stroke-linecap="round"/>'
            f'<circle cx="{550 + r*math.cos(a):.1f}" cy="{45 + r*math.sin(a):.1f}" r="1.8" fill="#c9a96e" opacity="0.55"/>'
        )
    h_lines = "".join(
        f'<line x1="{x}" y1="45" x2="{x+38}" y2="45" stroke="#c9a96e" stroke-width="0.5" opacity="0.2"/>'
        for side in [range(30, 480, 58), range(620, 1070, 58)]
        for x in side
    )
    return (
        f'<svg width="100%" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">'
        f'<defs>'
        f'<radialGradient id="hg" cx="50%" cy="50%" r="50%">'
        f'<stop offset="0%" stop-color="#c9a96e" stop-opacity="0.12"/>'
        f'<stop offset="100%" stop-color="#c9a96e" stop-opacity="0"/>'
        f'</radialGradient></defs>'
        f'{stars}'
        f'<circle cx="550" cy="45" r="48" fill="url(#hg)"/>'
        f'<circle cx="550" cy="45" r="40" fill="none" stroke="#c9a96e" stroke-width="0.5" opacity="0.28"/>'
        f'<circle cx="550" cy="45" r="22" fill="none" stroke="#c9a96e" stroke-width="0.9" opacity="0.4"/>'
        f'{arms}'
        f'<circle cx="550" cy="45" r="5" fill="#c9a96e" opacity="0.75"/>'
        f'{h_lines}'
        f'</svg>'
    )


def card_svg(card_name: str, w=110, h=165) -> str:
    rng = _rng(card_name)
    if "Wands" in card_name:
        c1, c2, c3 = "#3a1a0a", "#c47a2a", "#f2c060"
        sym_type = "wand"
    elif "Cups" in card_name:
        c1, c2, c3 = "#0a1e3a", "#2a6aaa", "#7ec4cc"
        sym_type = "cup"
    elif "Swords" in card_name:
        c1, c2, c3 = "#101828", "#4a6a8a", "#c4d4e4"
        sym_type = "sword"
    elif "Pentacles" in card_name:
        c1, c2, c3 = "#0a2a16", "#2a7a3a", "#8aca7a"
        sym_type = "pent"
    else:
        c1, c2, c3 = "#1a0a3a", "#7a3ab4", "#c49ae4"
        sym_type = "major"

    cx, cy = w // 2, h // 2
    stars = "".join(
        f'<circle cx="{rng.randint(4,w-4)}" cy="{rng.randint(4,h-4)}" r="{rng.uniform(0.4,1.6):.1f}" '
        f'fill="white" opacity="{rng.uniform(0.2,0.7):.2f}"/>'
        for _ in range(14)
    )
    sid = abs(hash(card_name)) % 9999

    if sym_type == "wand":
        sym = (
            f'<line x1="{cx}" y1="{cy-32}" x2="{cx}" y2="{cy+32}" stroke="{c3}" stroke-width="2.5" stroke-linecap="round"/>'
            f'<ellipse cx="{cx}" cy="{cy-35}" rx="5" ry="9" fill="{c2}" opacity="0.9"/>'
            f'<line x1="{cx-14}" y1="{cy-8}" x2="{cx+14}" y2="{cy-8}" stroke="{c3}" stroke-width="1.2" opacity="0.55"/>'
            f'<line x1="{cx-9}" y1="{cy+8}" x2="{cx+9}" y2="{cy+8}" stroke="{c3}" stroke-width="1.2" opacity="0.4"/>'
        )
    elif sym_type == "cup":
        sym = (
            f'<path d="M{cx-18} {cy-22} Q{cx-20} {cy+18} {cx} {cy+24} Q{cx+20} {cy+18} {cx+18} {cy-22} Z" '
            f'fill="none" stroke="{c3}" stroke-width="1.8"/>'
            f'<line x1="{cx-7}" y1="{cy+24}" x2="{cx+7}" y2="{cy+24}" stroke="{c3}" stroke-width="2"/>'
            f'<line x1="{cx}" y1="{cy+24}" x2="{cx}" y2="{cy+34}" stroke="{c3}" stroke-width="2"/>'
            f'<ellipse cx="{cx}" cy="{cy+34}" rx="10" ry="2" fill="{c3}" opacity="0.4"/>'
        )
    elif sym_type == "sword":
        sym = (
            f'<line x1="{cx}" y1="{cy-35}" x2="{cx}" y2="{cy+22}" stroke="{c3}" stroke-width="2" stroke-linecap="round"/>'
            f'<polygon points="{cx},{cy-38} {cx-4},{cy-12} {cx+4},{cy-12}" fill="{c3}"/>'
            f'<line x1="{cx-15}" y1="{cy+18}" x2="{cx+15}" y2="{cy+18}" stroke="{c3}" stroke-width="2.5" stroke-linecap="round"/>'
            f'<circle cx="{cx}" cy="{cy+28}" r="4" fill="{c2}" stroke="{c3}" stroke-width="1.2"/>'
        )
    elif sym_type == "pent":
        pts = [(cx + 22*math.cos(math.radians(-90 + i*72)), cy + 22*math.sin(math.radians(-90 + i*72))) for i in range(5)]
        path = f"M{pts[0][0]:.1f},{pts[0][1]:.1f} L{pts[2][0]:.1f},{pts[2][1]:.1f} L{pts[4][0]:.1f},{pts[4][1]:.1f} L{pts[1][0]:.1f},{pts[1][1]:.1f} L{pts[3][0]:.1f},{pts[3][1]:.1f} Z"
        sym = (
            f'<path d="{path}" fill="none" stroke="{c3}" stroke-width="1.5"/>'
            f'<circle cx="{cx}" cy="{cy}" r="26" fill="none" stroke="{c3}" stroke-width="0.8" opacity="0.45"/>'
        )
    else:
        sym = (
            f'<circle cx="{cx}" cy="{cy}" r="28" fill="none" stroke="{c3}" stroke-width="0.9" opacity="0.45"/>'
            f'<circle cx="{cx}" cy="{cy}" r="17" fill="none" stroke="{c2}" stroke-width="1.5" opacity="0.7"/>'
            f'<circle cx="{cx}" cy="{cy}" r="5" fill="{c2}" opacity="0.85"/>'
            f'<line x1="{cx-28}" y1="{cy}" x2="{cx+28}" y2="{cy}" stroke="{c3}" stroke-width="0.6" opacity="0.4"/>'
            f'<line x1="{cx}" y1="{cy-28}" x2="{cx}" y2="{cy+28}" stroke="{c3}" stroke-width="0.6" opacity="0.4"/>'
        )

    dot_ring = "".join(
        f'<circle cx="{cx + 44*math.cos(math.radians(i*45)):.1f}" cy="{cy + 70*math.sin(math.radians(i*45)):.1f}" '
        f'r="1.4" fill="{c3}" opacity="0.45"/>'
        for i in range(8)
    )

    return (
        f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">'
        f'<defs>'
        f'<linearGradient id="cbg{sid}" x1="0%" y1="0%" x2="100%" y2="100%">'
        f'<stop offset="0%" stop-color="{c1}"/><stop offset="100%" stop-color="{c1}" stop-opacity="0.7"/>'
        f'</linearGradient>'
        f'<filter id="cg{sid}"><feGaussianBlur stdDeviation="2.5" result="b"/>'
        f'<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
        f'</defs>'
        f'<rect width="{w}" height="{h}" fill="url(#cbg{sid})" rx="6"/>'
        f'<rect x="3" y="3" width="{w-6}" height="{h-6}" fill="none" stroke="{c3}" stroke-width="0.7" rx="4" opacity="0.45"/>'
        f'<rect x="6" y="6" width="{w-12}" height="{h-12}" fill="none" stroke="{c3}" stroke-width="0.35" rx="3" opacity="0.25"/>'
        f'{stars}'
        f'<g filter="url(#cg{sid})">{sym}</g>'
        f'{dot_ring}'
        f'</svg>'
    )


def ornament_svg(width="100%") -> str:
    return (
        '<svg width="' + str(width) + '" height="18" viewBox="0 0 400 18" xmlns="http://www.w3.org/2000/svg">'
        '<line x1="0" y1="9" x2="175" y2="9" stroke="#c9a96e" stroke-width="0.6" opacity="0.35"/>'
        '<circle cx="185" cy="9" r="2" fill="#c9a96e" opacity="0.5"/>'
        '<circle cx="195" cy="9" r="3.5" fill="#c9a96e" opacity="0.6"/>'
        '<circle cx="205" cy="9" r="2" fill="#c9a96e" opacity="0.5"/>'
        '<line x1="215" y1="9" x2="400" y2="9" stroke="#c9a96e" stroke-width="0.6" opacity="0.35"/>'
        '</svg>'
    )


def number_card_html(label: str, number: int, title: str, meaning: str, is_master: bool) -> str:
    master_badge = '<div class="num-card-master">✦ Master Number</div>' if is_master else ""
    return (
        f'<div class="num-card">'
        f'<p class="num-card-label">{label}</p>'
        f'<p class="num-card-number">{number}</p>'
        f'<p class="num-card-title">{title}</p>'
        f'{master_badge}'
        f'<p class="num-card-meaning">{meaning}</p>'
        f'</div>'
    )


def famous_people_html(number: int) -> str:
    people = FAMOUS_PEOPLE.get(number, [])
    if not people:
        return ""
    cards = ""
    for p in people:
        initials = "".join(w[0] for w in p["name"].split()[:2]).upper()
        cards += (
            f'<div class="person-card">'
            f'<div class="person-avatar">{initials}</div>'
            f'<p class="person-name">{p["name"]}</p>'
            f'<p class="person-desc">{p["desc"]}</p>'
            f'<a class="person-link" href="{p["url"]}" target="_blank">→ Wikipedia</a>'
            f'</div>'
        )
    return (
        f'<div style="margin-top:18px;">'
        f'<p style="font-family:\'Space Grotesk\',sans-serif;font-size:0.72rem;'
        f'letter-spacing:0.1em;text-transform:uppercase;color:#6a8a9a;margin-bottom:8px;">'
        f'Famous Life Path {number}s</p>'
        f'<div class="person-grid">{cards}</div>'
        f'</div>'
    )


# ── Data ──────────────────────────────────────────────────────────────────────

tarot_deck = [
    "The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor",
    "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit",
    "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance",
    "The Devil", "The Tower", "The Star", "The Moon", "The Sun", "Judgement", "The World"
]
suits = ["Wands", "Cups", "Swords", "Pentacles"]
ranks = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Page", "Knight", "Queen", "King"]
for suit in suits:
    for rank in ranks:
        tarot_deck.append(f"{rank} of {suit}")

MASTER_NUMBERS = {11, 22, 33}

PYTHAGOREAN = {
    'A':1,'B':2,'C':3,'D':4,'E':5,'F':6,'G':7,'H':8,'I':9,
    'J':1,'K':2,'L':3,'M':4,'N':5,'O':6,'P':7,'Q':8,'R':9,
    'S':1,'T':2,'U':3,'V':4,'W':5,'X':6,'Y':7,'Z':8,
}
VOWELS = set('AEIOU')

NUMBER_MEANINGS = {
    1:  ("The Pioneer",        "Leadership, independence, new beginnings, ambition, originality."),
    2:  ("The Diplomat",       "Partnership, balance, sensitivity, cooperation, intuition."),
    3:  ("The Expresser",      "Creativity, joy, self-expression, communication, optimism."),
    4:  ("The Builder",        "Stability, hard work, discipline, foundation, practicality."),
    5:  ("The Adventurer",     "Freedom, change, adventure, versatility, curiosity."),
    6:  ("The Nurturer",       "Responsibility, harmony, nurturing, care, domesticity."),
    7:  ("The Seeker",         "Spirituality, introspection, wisdom, analysis, mysticism."),
    8:  ("The Powerhouse",     "Abundance, material success, authority, power, achievement."),
    9:  ("The Humanitarian",   "Compassion, completion, universal love, philanthropy, wisdom."),
    11: ("The Illuminator",    "Master Number — heightened intuition, spiritual insight, inspiration, visionary."),
    22: ("The Master Builder", "Master Number — practical visionary, large-scale ambitions, transformational leadership."),
    33: ("The Master Teacher", "Master Number — compassionate service, healing, uplifting humanity."),
}

FAMOUS_PEOPLE = {
    1: [
        {"name": "Steve Jobs",           "desc": "Visionary co-founder of Apple",        "url": "https://en.wikipedia.org/wiki/Steve_Jobs"},
        {"name": "Martin Luther King Jr.","desc": "Civil rights pioneer & orator",        "url": "https://en.wikipedia.org/wiki/Martin_Luther_King_Jr."},
        {"name": "Nikola Tesla",          "desc": "Revolutionary electrical inventor",     "url": "https://en.wikipedia.org/wiki/Nikola_Tesla"},
        {"name": "Tom Hanks",             "desc": "Oscar-winning actor & storyteller",     "url": "https://en.wikipedia.org/wiki/Tom_Hanks"},
        {"name": "George Washington",     "desc": "First US President",                    "url": "https://en.wikipedia.org/wiki/George_Washington"},
    ],
    2: [
        {"name": "Barack Obama",   "desc": "44th US President, diplomat",       "url": "https://en.wikipedia.org/wiki/Barack_Obama"},
        {"name": "Bill Clinton",   "desc": "42nd US President",                  "url": "https://en.wikipedia.org/wiki/Bill_Clinton"},
        {"name": "Jennifer Aniston","desc":"Beloved actress & cultural icon",    "url": "https://en.wikipedia.org/wiki/Jennifer_Aniston"},
        {"name": "Tony Blair",     "desc": "British Prime Minister",             "url": "https://en.wikipedia.org/wiki/Tony_Blair"},
        {"name": "Meg Ryan",       "desc": "Iconic romantic film actress",       "url": "https://en.wikipedia.org/wiki/Meg_Ryan"},
    ],
    3: [
        {"name": "David Bowie",       "desc": "Rock legend & shape-shifter",        "url": "https://en.wikipedia.org/wiki/David_Bowie"},
        {"name": "Celine Dion",       "desc": "Powerhouse vocalist",                "url": "https://en.wikipedia.org/wiki/Celine_Dion"},
        {"name": "John Travolta",     "desc": "Dancer, actor & icon",               "url": "https://en.wikipedia.org/wiki/John_Travolta"},
        {"name": "Christina Aguilera","desc": "Grammy-winning pop singer",          "url": "https://en.wikipedia.org/wiki/Christina_Aguilera"},
        {"name": "Snoop Dogg",        "desc": "Rap legend & entertainer",           "url": "https://en.wikipedia.org/wiki/Snoop_Dogg"},
    ],
    4: [
        {"name": "Oprah Winfrey",       "desc": "Media mogul & philanthropist",      "url": "https://en.wikipedia.org/wiki/Oprah_Winfrey"},
        {"name": "Bill Gates",          "desc": "Microsoft co-founder",              "url": "https://en.wikipedia.org/wiki/Bill_Gates"},
        {"name": "Brad Pitt",           "desc": "Actor & producer",                  "url": "https://en.wikipedia.org/wiki/Brad_Pitt"},
        {"name": "Clint Eastwood",      "desc": "Legendary actor-director",          "url": "https://en.wikipedia.org/wiki/Clint_Eastwood"},
        {"name": "Arnold Schwarzenegger","desc":"Actor & California Governor",       "url": "https://en.wikipedia.org/wiki/Arnold_Schwarzenegger"},
    ],
    5: [
        {"name": "Beyoncé",          "desc": "Queen of pop, singer & actress",    "url": "https://en.wikipedia.org/wiki/Beyonc%C3%A9"},
        {"name": "Abraham Lincoln",  "desc": "16th US President, emancipator",    "url": "https://en.wikipedia.org/wiki/Abraham_Lincoln"},
        {"name": "Steven Spielberg", "desc": "Master filmmaker",                  "url": "https://en.wikipedia.org/wiki/Steven_Spielberg"},
        {"name": "Mick Jagger",      "desc": "Rolling Stones frontman",           "url": "https://en.wikipedia.org/wiki/Mick_Jagger"},
        {"name": "Vincent van Gogh", "desc": "Post-impressionist painter",        "url": "https://en.wikipedia.org/wiki/Vincent_van_Gogh"},
    ],
    6: [
        {"name": "John Lennon",     "desc": "Beatles legend & peace activist",   "url": "https://en.wikipedia.org/wiki/John_Lennon"},
        {"name": "Albert Einstein", "desc": "Theoretical physicist, Nobel laureate","url":"https://en.wikipedia.org/wiki/Albert_Einstein"},
        {"name": "Michael Jackson", "desc": "King of Pop",                        "url": "https://en.wikipedia.org/wiki/Michael_Jackson"},
        {"name": "Marilyn Monroe",  "desc": "Hollywood icon & actress",           "url": "https://en.wikipedia.org/wiki/Marilyn_Monroe"},
        {"name": "Bruce Lee",       "desc": "Martial arts legend & philosopher",  "url": "https://en.wikipedia.org/wiki/Bruce_Lee"},
    ],
    7: [
        {"name": "Princess Diana",    "desc": "People's Princess, humanitarian",  "url": "https://en.wikipedia.org/wiki/Diana,_Princess_of_Wales"},
        {"name": "Taylor Swift",      "desc": "Songwriter & cultural phenomenon", "url": "https://en.wikipedia.org/wiki/Taylor_Swift"},
        {"name": "Leonardo DiCaprio", "desc": "Oscar-winning actor",              "url": "https://en.wikipedia.org/wiki/Leonardo_DiCaprio"},
        {"name": "Natalie Portman",   "desc": "Oscar-winning actress",            "url": "https://en.wikipedia.org/wiki/Natalie_Portman"},
        {"name": "Katy Perry",        "desc": "Pop star & entertainer",           "url": "https://en.wikipedia.org/wiki/Katy_Perry"},
    ],
    8: [
        {"name": "Pablo Picasso",   "desc": "Cubism pioneer & artistic genius",  "url": "https://en.wikipedia.org/wiki/Pablo_Picasso"},
        {"name": "Nelson Mandela",  "desc": "Anti-apartheid revolutionary",       "url": "https://en.wikipedia.org/wiki/Nelson_Mandela"},
        {"name": "Sandra Bullock",  "desc": "Oscar-winning actress",             "url": "https://en.wikipedia.org/wiki/Sandra_Bullock"},
        {"name": "Martha Stewart",  "desc": "Lifestyle entrepreneur & author",   "url": "https://en.wikipedia.org/wiki/Martha_Stewart"},
        {"name": "50 Cent",         "desc": "Rapper & entrepreneur",             "url": "https://en.wikipedia.org/wiki/50_Cent"},
    ],
    9: [
        {"name": "Mahatma Gandhi",  "desc": "Father of nonviolent resistance",   "url": "https://en.wikipedia.org/wiki/Mahatma_Gandhi"},
        {"name": "Morgan Freeman",  "desc": "Iconic actor & narrator",           "url": "https://en.wikipedia.org/wiki/Morgan_Freeman"},
        {"name": "Bob Marley",      "desc": "Reggae legend & global icon",       "url": "https://en.wikipedia.org/wiki/Bob_Marley"},
        {"name": "Jim Carrey",      "desc": "Comedian, actor & philosopher",     "url": "https://en.wikipedia.org/wiki/Jim_Carrey"},
        {"name": "Whitney Houston", "desc": "Legendary vocalist",                "url": "https://en.wikipedia.org/wiki/Whitney_Houston"},
    ],
    11: [
        {"name": "Prince",                 "desc": "Musical genius & icon",          "url": "https://en.wikipedia.org/wiki/Prince_(musician)"},
        {"name": "Michelle Obama",         "desc": "Former First Lady & author",      "url": "https://en.wikipedia.org/wiki/Michelle_Obama"},
        {"name": "Orlando Bloom",          "desc": "Actor & humanitarian",            "url": "https://en.wikipedia.org/wiki/Orlando_Bloom"},
        {"name": "Edgar Allan Poe",        "desc": "Master of Gothic literature",     "url": "https://en.wikipedia.org/wiki/Edgar_Allan_Poe"},
        {"name": "Hans Christian Andersen","desc": "Author of beloved fairy tales",   "url": "https://en.wikipedia.org/wiki/Hans_Christian_Andersen"},
    ],
    22: [
        {"name": "Will Smith",    "desc": "Actor & hip-hop artist",         "url": "https://en.wikipedia.org/wiki/Will_Smith"},
        {"name": "Paul McCartney","desc": "Beatles legend & composer",      "url": "https://en.wikipedia.org/wiki/Paul_McCartney"},
        {"name": "Tina Turner",   "desc": "Queen of Rock & Roll",           "url": "https://en.wikipedia.org/wiki/Tina_Turner"},
        {"name": "Dean Martin",   "desc": "Rat Pack entertainer",           "url": "https://en.wikipedia.org/wiki/Dean_Martin"},
        {"name": "Lucille Ball",  "desc": "Comedy pioneer & TV icon",       "url": "https://en.wikipedia.org/wiki/Lucille_Ball"},
    ],
    33: [
        {"name": "Stephen King",         "desc": "Master of horror & fiction",         "url": "https://en.wikipedia.org/wiki/Stephen_King"},
        {"name": "Meryl Streep",         "desc": "Most nominated actress in history",   "url": "https://en.wikipedia.org/wiki/Meryl_Streep"},
        {"name": "Francis Ford Coppola", "desc": "Director of The Godfather",           "url": "https://en.wikipedia.org/wiki/Francis_Ford_Coppola"},
        {"name": "Robert De Niro",       "desc": "Legendary method actor",              "url": "https://en.wikipedia.org/wiki/Robert_De_Niro"},
        {"name": "Deepak Chopra",        "desc": "Author & wellness pioneer",           "url": "https://en.wikipedia.org/wiki/Deepak_Chopra"},
    ],
}

spread_types = {
    "Celtic Cross": {
        "num_cards": 10,
        "positions": [
            "Present — The Veil of Now",
            "Challenge — The Shadow's Whisper",
            "Past — Echoes of Yesterday",
            "Future — Tomorrow's Mist",
            "Above — The Conscious Realm",
            "Below — Subconscious Depths",
            "Advice — The Inner Voice",
            "External — Cosmic Winds",
            "Hopes & Fears — Heart's Duality",
            "Outcome — The Tapestry's End",
        ],
    },
    "Three-Card Spread": {
        "num_cards": 3,
        "positions": ["Past — Echoes of Time", "Present — Current Nexus", "Future — Unfolding Path"],
    },
    "Elemental Spread": {
        "num_cards": 5,
        "positions": [
            "Fire — Passion & Energy",
            "Water — Emotions & Intuition",
            "Air — Thoughts & Communication",
            "Earth — Material & Practical",
            "Spirit — Higher Purpose",
        ],
    },
}

QUOTES = [
    "The universe whispers its secrets to those who listen with their heart.",
    "In the tapestry of fate, every thread has its purpose.",
    "The cards reveal not your destiny, but the path to shape it.",
    "As above, so below; as within, so without.",
    "The greatest magic lies in understanding oneself.",
    "Stillness is where wisdom takes root.",
    "Every ending is a threshold to something yet unnamed.",
]


# ── Numerology helpers ────────────────────────────────────────────────────────

def reduce_to_single_digit(n: int) -> int:
    while n > 9 and n not in MASTER_NUMBERS:
        n = sum(int(d) for d in str(n))
    return n


def calculate_life_path_number(birth_date) -> int:
    m = reduce_to_single_digit(birth_date.month)
    d = reduce_to_single_digit(birth_date.day)
    y = reduce_to_single_digit(sum(int(c) for c in str(birth_date.year)))
    return reduce_to_single_digit(m + d + y)


def calculate_name_numbers(name: str):
    letters = [c for c in name.upper() if c.isalpha()]
    all_vals   = [PYTHAGOREAN.get(c, 0) for c in letters]
    vowel_vals = [PYTHAGOREAN.get(c, 0) for c in letters if c in VOWELS]
    cons_vals  = [PYTHAGOREAN.get(c, 0) for c in letters if c not in VOWELS]
    expression  = reduce_to_single_digit(sum(all_vals))
    soul_urge   = reduce_to_single_digit(sum(vowel_vals)) if vowel_vals else 0
    personality = reduce_to_single_digit(sum(cons_vals))  if cons_vals  else 0
    return expression, soul_urge, personality


# ── Header ────────────────────────────────────────────────────────────────────

st.markdown(f'<div style="margin-bottom:-12px">{header_svg()}</div>', unsafe_allow_html=True)
st.markdown("# Mystical Tarot de Multiverse")
st.markdown(
    '<p style="color:#6a8a9a;font-family:\'Space Grotesk\',sans-serif;font-size:0.8rem;'
    'letter-spacing:0.15em;text-transform:uppercase;margin-top:-8px;margin-bottom:24px;">'
    'Free Tarot &nbsp;·&nbsp; Numerology &nbsp;·&nbsp; Cosmic Readings</p>',
    unsafe_allow_html=True,
)

# ── Sidebar ───────────────────────────────────────────────────────────────────

st.sidebar.markdown("## Support the Creator")
st.sidebar.markdown(
    '<p style="font-size:0.95rem;line-height:1.7;color:#b0b8c8;">'
    'A free spirit in the poetry of code and cosmos — passionate about earth, '
    'wonder, and helping you find answers beautifully absurd.</p>',
    unsafe_allow_html=True,
)
st.sidebar.markdown(
    '<a href="https://buymeacoffee.com/yashvinishz" target="_blank" '
    'style="display:inline-block;background:linear-gradient(135deg,rgba(201,169,110,0.15),'
    'rgba(126,196,204,0.1));border:1px solid rgba(201,169,110,0.4);color:#c9a96e;'
    'font-family:\'Space Grotesk\',sans-serif;font-size:0.72rem;letter-spacing:0.1em;'
    'text-transform:uppercase;padding:10px 20px;border-radius:3px;text-decoration:none;">'
    'Bestow a Molly ✦</a>',
    unsafe_allow_html=True,
)
st.sidebar.markdown(
    '<p style="font-size:0.88rem;color:#6a8a9a;margin-top:12px;">'
    'Your love means the world. May you never run out of magic.</p>',
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")
st.sidebar.markdown(
    '<p style="font-family:\'Cinzel Decorative\',serif;font-size:0.65rem;'
    'color:#2d4a5a;letter-spacing:0.1em;text-align:center;text-transform:uppercase;">'
    'ᚠ ᚢ ᚦ ᚨ ᚱ ᚲ ᚷ ᚹ</p>',
    unsafe_allow_html=True,
)

# ── Tabs ──────────────────────────────────────────────────────────────────────

tarot_tab, numerology_tab, wisdom_tab = st.tabs(["✦ Tarot Reading", "✦ Numerology", "✦ Ancient Wisdom"])

# ════════════════════════════════════════════════════════════════════════════
# TAROT TAB
# ════════════════════════════════════════════════════════════════════════════
with tarot_tab:
    st.markdown(
        '<p style="color:#8a9aac;font-size:1.05rem;max-width:640px;margin-bottom:28px;">'
        'The cards are a mirror held up to the soul — not a cage, but a lantern. '
        'Breathe. Ask what stirs inside you, and let the cosmos answer.</p>',
        unsafe_allow_html=True,
    )

    col_q, col_s = st.columns([3, 2], gap="large")
    with col_q:
        st.markdown("## Whisper Your Question")
        question = st.text_input(
            "Your question",
            placeholder="What does the universe want me to know about…",
            label_visibility="collapsed",
        )
    with col_s:
        st.markdown("## Choose Your Spread")
        spread_type = st.selectbox(
            "Spread",
            list(spread_types.keys()),
            label_visibility="collapsed",
        )

    st.markdown(f'<div style="margin:20px 0 8px">{ornament_svg()}</div>', unsafe_allow_html=True)

    if st.button(f"Unveil the {spread_type}"):
        if not question:
            st.warning("Please whisper your question to the universe before seeking its wisdom.")
        else:
            with st.spinner("The cards are dancing in the ethereal realm…"):
                random.shuffle(tarot_deck)
                spread = random.sample(tarot_deck, spread_types[spread_type]["num_cards"])
                positions = spread_types[spread_type]["positions"]

            st.markdown(
                f'<p style="color:#6a8a9a;font-family:\'Space Grotesk\',sans-serif;'
                f'font-size:0.78rem;letter-spacing:0.1em;text-transform:uppercase;'
                f'margin-bottom:4px;">Your Query</p>'
                f'<p style="font-size:1.15rem;color:#e8dcc8;font-style:italic;'
                f'margin-bottom:28px;">&ldquo;{question}&rdquo;</p>',
                unsafe_allow_html=True,
            )

            st.markdown(f"## The {spread_type}")
            n = len(spread)
            cols = st.columns(min(n, 5))
            for i, (card, pos) in enumerate(zip(spread, positions)):
                with cols[i % min(n, 5)]:
                    svg = card_svg(card)
                    short_pos = pos.split("—")[0].strip()
                    st.markdown(
                        f'<div class="tarot-card">'
                        f'<p class="tarot-pos">{short_pos}</p>'
                        f'{svg}'
                        f'<p class="tarot-name">{card}</p>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

            spread_description = "\n".join(f"{pos}: {card}" for pos, card in zip(positions, spread))
            prompt = (
                f"As a mystical sage, interpret this {spread_type} tarot spread:\n{spread_description}\n\n"
                f"Cosmic Question: {question}\n\n"
                "Weave a tapestry of wisdom, revealing hidden threads of fate. Include specific card meanings "
                "and their interactions. Be warm, specific, and directly answer the question. "
                "End with a light-hearted pun."
            )
            st.markdown(f'<div style="margin:28px 0 8px">{ornament_svg()}</div>', unsafe_allow_html=True)
            st.markdown("## Cosmic Interpretation")
            with st.spinner("The cosmic energies are aligning…"):
                try:
                    resp = openai.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": prompt}],
                    )
                    interpretation = resp.choices[0].message.content.strip()
                    for para in interpretation.split("\n\n"):
                        if para.strip():
                            st.markdown(
                                f'<div class="interp-para">{para.strip()}</div>',
                                unsafe_allow_html=True,
                            )
                except Exception:
                    st.info("AI interpretation is unavailable right now — your cards carry all the wisdom you need.")

            st.markdown(
                f'<p style="text-align:center;font-style:italic;color:#4a6a7a;'
                f'font-size:0.95rem;margin-top:24px;">&ldquo;{random.choice(QUOTES)}&rdquo;</p>',
                unsafe_allow_html=True,
            )
            st.info("Found this reading helpful? Slip to the sidebar — molly awaits. 🥰")


# ════════════════════════════════════════════════════════════════════════════
# NUMEROLOGY TAB
# ════════════════════════════════════════════════════════════════════════════
with numerology_tab:
    st.markdown(
        '<p style="color:#8a9aac;font-size:1.05rem;max-width:680px;margin-bottom:28px;">'
        'Numbers are the language the cosmos uses to describe itself. '
        'Enter your birth date and name to decode the vibrational blueprint of your soul.</p>',
        unsafe_allow_html=True,
    )

    col_l, col_r = st.columns(2, gap="large")
    with col_l:
        st.markdown("## Your Birth Date")
        birth_date = st.date_input(
            "Birth Date",
            value=None,
            min_value=datetime(1900, 1, 1).date(),
            max_value=datetime.today().date(),
            label_visibility="collapsed",
        )
    with col_r:
        st.markdown("## Your Full Name")
        full_name = st.text_input(
            "Full name at birth",
            placeholder="e.g. Jane Marie Doe",
            label_visibility="collapsed",
        )

    st.markdown(f'<div style="margin:20px 0 8px">{ornament_svg()}</div>', unsafe_allow_html=True)

    if st.button("Reveal My Numbers"):
        if not birth_date and not (full_name and full_name.strip()):
            st.warning("Please enter your birth date or full name to begin your reading.")
        else:
            # ── Life Path ──────────────────────────────────────────────
            if birth_date:
                life_path = calculate_life_path_number(birth_date)
                lp_title, lp_meaning = NUMBER_MEANINGS.get(life_path, ("Unknown", "—"))
                st.markdown("## Life Path Number")
                st.markdown(
                    '<p style="color:#8a9aac;font-size:0.95rem;max-width:600px;margin-bottom:16px;">'
                    'Your Life Path Number is the most significant in your chart — '
                    'the overarching theme your soul chose for this incarnation.</p>',
                    unsafe_allow_html=True,
                )
                lp_col, _, __ = st.columns([1, 1, 1])
                with lp_col:
                    st.markdown(
                        number_card_html("Life Path", life_path, lp_title, lp_meaning, life_path in MASTER_NUMBERS),
                        unsafe_allow_html=True,
                    )
                st.markdown(famous_people_html(life_path), unsafe_allow_html=True)

            # ── Name Numbers ───────────────────────────────────────────
            if full_name and full_name.strip():
                expression, soul_urge, personality = calculate_name_numbers(full_name.strip())
                st.markdown(f'<div style="margin:32px 0 8px">{ornament_svg()}</div>', unsafe_allow_html=True)
                st.markdown("## Name Numbers")
                st.markdown(
                    '<p style="color:#8a9aac;font-size:0.95rem;max-width:640px;margin-bottom:16px;">'
                    'Your name vibrates with three energies: '
                    '<em>Expression</em> (full potential), '
                    '<em>Soul Urge</em> (deepest desires from vowels), and '
                    '<em>Personality</em> (how others perceive you from consonants).</p>',
                    unsafe_allow_html=True,
                )
                nc1, nc2, nc3 = st.columns(3, gap="medium")
                with nc1:
                    et, em = NUMBER_MEANINGS.get(expression, ("Unknown", "—"))
                    st.markdown(number_card_html("Expression", expression, et, em, expression in MASTER_NUMBERS), unsafe_allow_html=True)
                with nc2:
                    su_title2, su_meaning2 = NUMBER_MEANINGS.get(soul_urge, ("Unknown", "—"))
                    st.markdown(number_card_html("Soul Urge", soul_urge, su_title2, su_meaning2, soul_urge in MASTER_NUMBERS), unsafe_allow_html=True)
                with nc3:
                    pt, pm = NUMBER_MEANINGS.get(personality, ("Unknown", "—"))
                    st.markdown(number_card_html("Personality", personality, pt, pm, personality in MASTER_NUMBERS), unsafe_allow_html=True)

            # ── AI Interpretation ──────────────────────────────────────
            st.markdown(f'<div style="margin:32px 0 8px">{ornament_svg()}</div>', unsafe_allow_html=True)
            st.markdown("## Cosmic Numerology Reading")

            num_parts = []
            if birth_date:
                lp_t, lp_m = NUMBER_MEANINGS.get(life_path, ("",""))
                num_parts.append(f"Life Path {life_path} ({lp_t}): {lp_m}")
            if full_name and full_name.strip():
                et, em = NUMBER_MEANINGS.get(expression, ("",""))
                su_t, su_m = NUMBER_MEANINGS.get(soul_urge, ("",""))
                pe_t, pe_m = NUMBER_MEANINGS.get(personality, ("",""))
                num_parts.append(f"Expression {expression} ({et}): {em}")
                num_parts.append(f"Soul Urge {soul_urge} ({su_t}): {su_m}")
                num_parts.append(f"Personality {personality} ({pe_t}): {pe_m}")

            name_clause = f" for {full_name.strip()}" if full_name and full_name.strip() else ""
            date_clause = f" born on {birth_date.strftime('%B %d, %Y')}" if birth_date else ""
            numerology_prompt = (
                f"You are a mystical numerologist. Provide a rich, personalised numerology reading"
                f"{name_clause}{date_clause}.\n\nTheir numbers:\n" + "\n".join(num_parts) + "\n\n"
                "Weave the numbers into a cohesive cosmic narrative. Highlight how they complement "
                "or tension with each other, reveal soul purpose, strengths, and challenges. "
                "Be warm, insightful, specific. End with an encouraging note and a numerology pun."
            )

            with st.spinner("The numbers are aligning in the cosmic grid…"):
                try:
                    num_resp = openai.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": numerology_prompt}],
                    )
                    interp = num_resp.choices[0].message.content.strip()
                    for para in interp.split("\n\n"):
                        if para.strip():
                            st.markdown(
                                f'<div class="interp-para">{para.strip()}</div>',
                                unsafe_allow_html=True,
                            )
                except Exception:
                    st.info("AI interpretation is unavailable right now. Your numbers carry all the wisdom needed.")

            st.info("Found this reading helpful? Slip to the sidebar — molly awaits. 🥰")


# ════════════════════════════════════════════════════════════════════════════
# WISDOM TAB
# ════════════════════════════════════════════════════════════════════════════
with wisdom_tab:
    st.markdown("## The Ancient Wisdom of Numerology")
    st.markdown(f'<div style="margin:4px 0 20px">{ornament_svg()}</div>', unsafe_allow_html=True)

    col_w1, col_w2 = st.columns([3, 2], gap="large")
    with col_w1:
        st.markdown(
            '<p style="font-size:1.06rem;line-height:1.8;color:#c8d8e0;">'
            'Numerology is one of humanity\'s oldest metaphysical sciences, tracing its roots to ancient '
            'Babylon, Egypt, and Greece. The philosopher Pythagoras (569–490 BCE) formalised numerology '
            'in the Western tradition, teaching that numbers are the fundamental building blocks of the '
            'universe — each carrying a unique vibrational essence that shapes personality, life events, '
            'and spiritual evolution.</p>',
            unsafe_allow_html=True,
        )
        st.markdown("### The Core Numbers")
        for label, desc in [
            ("Life Path", "Derived from your birth date — your cosmic fingerprint and the overarching theme of your incarnation."),
            ("Expression", "Calculated from all letters of your full birth name — the talents and abilities you came to express."),
            ("Soul Urge",  "Drawn from the vowels — the deepest longings of your soul, what you truly crave at a heart level."),
            ("Personality","Formed by the consonants — the mask you wear and how others first perceive you."),
        ]:
            st.markdown(
                f'<div style="background:rgba(24,45,74,0.5);border-left:2px solid rgba(201,169,110,0.4);'
                f'border-radius:0 6px 6px 0;padding:12px 16px;margin-bottom:10px;">'
                f'<span style="font-family:\'Cinzel Decorative\',serif;font-size:0.72rem;color:#c9a96e;'
                f'letter-spacing:0.06em;">{label}</span>'
                f'<p style="margin:6px 0 0;color:#a0b8c8;font-size:0.97rem;line-height:1.6;">{desc}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )
        st.markdown("### Master Numbers")
        st.markdown(
            '<p style="color:#b0c0d0;font-size:1.02rem;line-height:1.75;">'
            '<strong style="color:#c9a96e;">11, 22, and 33</strong> are Master Numbers — carrying amplified '
            'energy and a higher spiritual calling. Those with Master Numbers often feel a profound sense '
            'of purpose, alongside greater challenges as the universe calls them to rise.</p>',
            unsafe_allow_html=True,
        )

    with col_w2:
        st.markdown("### Tarot & the Jungian Psyche")
        st.markdown(
            '<p style="color:#a0b4c4;font-size:0.97rem;line-height:1.8;">'
            'Carl Jung proposed that archetypes are innate, universal prototypes residing in the '
            'collective unconscious. Each tarot card embodies these archetypal energies — '
            'serving as a bridge between the conscious mind and the deeper psyche.</p>'
            '<p style="color:#a0b4c4;font-size:0.97rem;line-height:1.8;margin-top:12px;">'
            'When we engage with the cards, we tap into universal symbols, allowing a dialogue '
            'between our personal narratives and the broader human condition. The cards reveal '
            'not your destiny, but illuminate the path to shape it.</p>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div style="margin-top:20px;padding:18px;background:rgba(24,45,74,0.6);'
            'border:1px solid rgba(201,169,110,0.2);border-radius:8px;">'
            '<p style="font-family:\'Cinzel Decorative\',serif;font-size:0.65rem;color:#c9a96e;'
            'letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px;">Further Reading</p>'
            '<p style="margin:0;font-size:0.92rem;">'
            '<a href="https://labyrinthos.co/blogs/learn-tarot-with-labyrinthos-academy/carl-jung-and-jungian-archetypes-in-the-tarot-the-various-aspects-of-our-selves" '
            'target="_blank" style="color:#7ec4cc;text-decoration:none;">'
            '→ Jungian Archetypes in Tarot</a></p>'
            '<p style="margin:8px 0 0;font-size:0.92rem;">'
            '<a href="https://en.wikipedia.org/wiki/Numerology" target="_blank" '
            'style="color:#7ec4cc;text-decoration:none;">→ Numerology on Wikipedia</a></p>'
            '</div>',
            unsafe_allow_html=True,
        )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(f'<div style="margin:40px 0 12px">{ornament_svg()}</div>', unsafe_allow_html=True)
st.markdown(
    '<p style="text-align:center;font-family:\'Space Grotesk\',sans-serif;font-size:0.7rem;'
    'color:#2d4a5a;letter-spacing:0.12em;text-transform:uppercase;">'
    'Mystical Tarot de Multiverse &nbsp;·&nbsp; ᚠ ᚢ ᚦ ᚨ ᚱ ᚲ &nbsp;·&nbsp; '
    'Readings for the Soul &nbsp;·&nbsp; '
    '<a href="https://twitter.com/cacooleed" target="_blank" style="color:#2d4a5a;">@cacooleed</a>'
    '</p>',
    unsafe_allow_html=True,
)
