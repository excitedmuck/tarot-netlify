import streamlit as st
import random
import openai
from datetime import datetime
import os

st.set_page_config(
    page_title="Free Tarot & Numerology Readings | Mystical Tarot de Multiverse",
    page_icon="🔮",
    layout="wide"
)
# Set up OpenAI client
# Get the OpenAI API key from the Replit environment
openai.api_key = os.getenv("OPENAI_API_KEY")

# Tarot Deck (Major Arcana and Minor Arcana)
tarot_deck = [
    "The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor",
    "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit",
    "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance",
    "The Devil", "The Tower", "The Star", "The Moon", "The Sun", "Judgement", "The World"
]

# Minor Arcana (simplified - only aces through kings in the four suits)
suits = ["Wands", "Cups", "Swords", "Pentacles"]
ranks = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Page", "Knight", "Queen", "King"]

# Add Minor Arcana cards to the tarot_deck
for suit in suits:
    for rank in ranks:
        tarot_deck.append(f"{rank} of {suit}")

# ── Numerology helpers ──────────────────────────────────────────────────────

MASTER_NUMBERS = {11, 22, 33}

PYTHAGOREAN = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
    'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
    'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8,
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


def reduce_to_single_digit(n: int) -> int:
    """Reduce a number to a single digit, preserving master numbers 11, 22, 33."""
    while n > 9 and n not in MASTER_NUMBERS:
        n = sum(int(d) for d in str(n))
    return n


def calculate_life_path_number(birth_date) -> int:
    """Calculate Life Path Number by reducing month, day, and year separately."""
    m = reduce_to_single_digit(birth_date.month)
    d = reduce_to_single_digit(birth_date.day)
    y = reduce_to_single_digit(sum(int(c) for c in str(birth_date.year)))
    return reduce_to_single_digit(m + d + y)


def calculate_name_numbers(name: str):
    """Return (expression, soul_urge, personality) numbers for a given name."""
    letters = [c for c in name.upper() if c.isalpha()]
    all_vals  = [PYTHAGOREAN.get(c, 0) for c in letters]
    vowel_vals = [PYTHAGOREAN.get(c, 0) for c in letters if c in VOWELS]
    cons_vals  = [PYTHAGOREAN.get(c, 0) for c in letters if c not in VOWELS]

    expression  = reduce_to_single_digit(sum(all_vals))
    soul_urge   = reduce_to_single_digit(sum(vowel_vals)) if vowel_vals else 0
    personality = reduce_to_single_digit(sum(cons_vals))  if cons_vals  else 0
    return expression, soul_urge, personality


def number_card(label: str, number: int, col) -> None:
    """Render a styled numerology result card inside a Streamlit column."""
    title, meaning = NUMBER_MEANINGS.get(number, ("Unknown", "—"))
    master_tag = " ⭐ Master Number" if number in MASTER_NUMBERS else ""
    col.markdown(
        f"""
        <div style="border:1px solid #9b59b6; border-radius:12px; padding:16px; background:#1a0a2e; text-align:center;">
            <p style="color:#d7bde2; margin:0; font-size:0.85rem;">{label}</p>
            <p style="color:#f39c12; font-size:2.5rem; margin:4px 0; font-weight:bold;">{number}</p>
            <p style="color:#e8daef; margin:0; font-weight:600;">{title}{master_tag}</p>
            <p style="color:#d7bde2; font-size:0.82rem; margin-top:6px;">{meaning}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── Page header ─────────────────────────────────────────────────────────────

st.markdown("# ✨ Mystical Tarot de Multiverse - Free Tarot & Numerology Readings ✨")  # H1 tag for SEO

# Sidebar for PayPal
st.sidebar.markdown("## Support the Creator")  # H2 tag for section
st.sidebar.write("I'm a free bird in autopoeisis poetry of code and word, I'm passionate about earth observation in deed and word, I like helping you get answers truly absurd.")
st.sidebar.write("I'm trying to raise butterfly wings for my cacoon. If this app has helped you in any way, buy me a molly and give me a hug!")
st.sidebar.markdown("[Bestow Me a Molly](https://buymeacoffee.com/yashvinishz)")
st.sidebar.write("Your love means the world to me. So may you never run out of molly! 🥰😉")

# ── Tabs ─────────────────────────────────────────────────────────────────────

tarot_tab, numerology_tab = st.tabs(["🔮 Tarot Reading", "🔢 Numerology"])

# ════════════════════════════════════════════════════════════════════════════
# TAROT TAB
# ════════════════════════════════════════════════════════════════════════════
with tarot_tab:
    # Define spread types with images
    spread_types = {
        "Celtic Cross": {
            "num_cards": 10,
            "positions": [
                "Present (The Veil of Now)",
                "Challenge (The Shadow's Whisper)",
                "Past (Echoes of Yesterday)",
                "Future (Tomorrow's Mist)",
                "Above (The Conscious Realm)",
                "Below (The Subconscious Depths)",
                "Advice (The Inner Voice)",
                "External Influences (The Cosmic Winds)",
                "Hopes and Fears (The Heart's Duality)",
                "Outcome (The Tapestry's End)"
            ],
        },
        "Three-Card Spread": {
            "num_cards": 3,
            "positions": [
                "Past (The Echoes of Time)",
                "Present (The Current Nexus)",
                "Future (The Unfolding Path)"
            ],
        },
        "Elemental Spread": {
            "num_cards": 5,
            "positions": [
                "Fire (Passion and Energy)",
                "Water (Emotions and Intuition)",
                "Air (Thoughts and Communication)",
                "Earth (Material and Practical Matters)",
                "Spirit (Higher Purpose and Connection)"
            ],
        }
    }

    # Get the user's question
    st.markdown("## 🔮 Whisper Your Question to the Cosmos for a Tarot Reading")  # H2 tag with keywords
    question = st.text_input("Ask about love, career, or your cosmic path...")

    # Let the user choose the spread type
    st.markdown("## Choose Your Cosmic Spread for Mystical Insights")  # H2 tag with keywords
    spread_type = st.selectbox("Select a spread to unveil your destiny:", list(spread_types.keys()))

    if st.button(f"🌟 Unveil the {spread_type} 🌟"):
        if question:
            # Magical shuffling animation
            with st.spinner("The cards are dancing in the ethereal realm..."):
                st.balloons()
                random.shuffle(tarot_deck)
                spread = random.sample(tarot_deck, spread_types[spread_type]["num_cards"])

            # Get the positions for the chosen spread
            spread_positions = spread_types[spread_type]["positions"]

            # Display the question
            st.subheader("🌠 Your Cosmic Query 🌠")
            st.write(question)

            # Display the spread
            st.subheader(f"🔮 The {spread_type} 🔮")
            cols = st.columns(spread_types[spread_type]["num_cards"])
            for i in range(len(spread)):
                with cols[i]:
                    st.markdown(f"**{spread_positions[i]}**")
                    st.write(spread[i])

            # Prepare the prompt for OpenAI
            spread_description = '\n'.join([f"{spread_positions[i]}: {spread[i]}" for i in range(len(spread))])
            prompt = f"As a mystical sage, interpret this {spread_type} tarot spread:\n{spread_description}\n\nCosmic Question: {question}\n\nWeave a tapestry of wisdom, revealing the hidden threads of fate and the whispers of the universe in your interpretation. Include specific card meanings and their interactions, make the response as specific and personalised as possible and directly answer the question. Always end in a punny note."

            # Get a response from OpenAI
            with st.spinner("The cosmic energies are aligning to reveal your destiny..."):
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )

            # Print the interpretation
            st.markdown("## 🌌 Cosmic Interpretation of Your Tarot Spread 🌌")  # H2 tag with keywords
            interpretation = response.choices[0].message.content.strip()
            paragraphs = interpretation.split('\n\n')
            for paragraph in paragraphs:
                st.markdown(f"✨ {paragraph}")

            # Add a mystical quote
            quotes = [
                "The universe whispers its secrets to those who listen with their heart.",
                "In the tapestry of fate, every thread has its purpose.",
                "The cards reveal not your destiny, but the path to shape it.",
                "As above, so below; as within, so without.",
                "The greatest magic lies in understanding oneself."
            ]
            st.markdown(f"***\n*{random.choice(quotes)}*")

            # Reminder to support
            st.info("If you found this reading helpful, slip to the left panel and you might see molly 🥰, or be my x @cacooleed and hear my folly 😉🦜.")

        else:
            st.warning("🌙 Please whisper your question to the universe before seeking its wisdom.")

# ════════════════════════════════════════════════════════════════════════════
# NUMEROLOGY TAB
# ════════════════════════════════════════════════════════════════════════════
with numerology_tab:
    st.markdown("## 🔢 Discover Your Numerology Blueprint")
    st.write(
        "Numerology is the ancient study of numbers and their cosmic vibrations. "
        "Enter your birth date and full name to uncover the numbers that shape your soul's journey."
    )

    col_left, col_right = st.columns(2)
    with col_left:
        birth_date = st.date_input(
            "🎂 Your Birth Date",
            value=None,
            min_value=datetime(1900, 1, 1).date(),
            max_value=datetime.today().date(),
            help="Used to calculate your Life Path Number",
        )
    with col_right:
        full_name = st.text_input(
            "✍️ Your Full Name (as given at birth)",
            placeholder="e.g. Jane Marie Doe",
            help="Used to calculate Expression, Soul Urge, and Personality numbers",
        )

    if st.button("🌠 Reveal My Numbers 🌠"):
        if not birth_date and not full_name:
            st.warning("🌙 Please enter your birth date or full name to begin your numerology reading.")
        else:
            st.markdown("---")

            # ── Life Path Number ─────────────────────────────────────────────
            if birth_date:
                life_path = calculate_life_path_number(birth_date)
                st.markdown("### 🌍 Life Path Number")
                st.write(
                    "Your **Life Path Number** is the most significant number in your chart — "
                    "it reveals your life's purpose and the journey your soul chose."
                )
                lp_col1, lp_col2, lp_col3 = st.columns([1, 1, 1])
                number_card("Life Path", life_path, lp_col1)

            # ── Name Numbers ─────────────────────────────────────────────────
            if full_name and full_name.strip():
                expression, soul_urge, personality = calculate_name_numbers(full_name.strip())
                st.markdown("### 📛 Name Numbers")
                st.write(
                    "Your name vibrates with three distinct energies: "
                    "**Expression** (your full potential), "
                    "**Soul Urge** (your inner desires, from vowels), and "
                    "**Personality** (how others perceive you, from consonants)."
                )
                nc1, nc2, nc3 = st.columns(3)
                number_card("Expression Number",  expression,  nc1)
                number_card("Soul Urge Number",   soul_urge,   nc2)
                number_card("Personality Number", personality, nc3)

            # ── AI Interpretation ─────────────────────────────────────────────
            st.markdown("---")
            st.markdown("### 🌌 Cosmic Numerology Interpretation")

            num_parts = []
            if birth_date:
                lp_title, lp_meaning = NUMBER_MEANINGS.get(life_path, ("", ""))
                num_parts.append(f"Life Path Number {life_path} ({lp_title}): {lp_meaning}")
            if full_name and full_name.strip():
                expr_title, expr_meaning = NUMBER_MEANINGS.get(expression, ("", ""))
                su_title,   su_meaning   = NUMBER_MEANINGS.get(soul_urge,   ("", ""))
                per_title,  per_meaning  = NUMBER_MEANINGS.get(personality, ("", ""))
                num_parts.append(f"Expression Number {expression} ({expr_title}): {expr_meaning}")
                num_parts.append(f"Soul Urge Number {soul_urge} ({su_title}): {su_meaning}")
                num_parts.append(f"Personality Number {personality} ({per_title}): {per_meaning}")

            numbers_summary = "\n".join(num_parts)
            name_clause = f" for {full_name.strip()}" if full_name and full_name.strip() else ""
            date_clause = f" born on {birth_date.strftime('%B %d, %Y')}" if birth_date else ""

            numerology_prompt = (
                f"You are a mystical numerologist. Provide a rich, personalised numerology reading"
                f"{name_clause}{date_clause}.\n\n"
                f"Their numbers are:\n{numbers_summary}\n\n"
                "Weave together the meaning of these numbers into a cohesive cosmic narrative. "
                "Highlight how they complement or tension with each other, reveal the person's "
                "soul purpose, strengths, and challenges. Be warm, insightful, and specific. "
                "End with an encouraging note and a light-hearted numerology pun."
            )

            with st.spinner("The numbers are aligning in the cosmic grid..."):
                try:
                    num_response = openai.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": numerology_prompt}]
                    )
                    interpretation = num_response.choices[0].message.content.strip()
                    for para in interpretation.split('\n\n'):
                        st.markdown(f"✨ {para}")
                except Exception:
                    st.info(
                        "AI interpretation is unavailable right now. "
                        "Your numbers above carry all the cosmic wisdom you need! 🌟"
                    )

            st.markdown("***")
            st.info("If you found this reading helpful, slip to the left panel and you might see molly 🥰, or be my x @cacooleed and hear my folly 😉🦜.")

    # Educational content about numerology
    st.markdown("---")
    st.markdown("## The Ancient Wisdom of Numerology")
    st.write("""
Numerology is one of humanity's oldest metaphysical sciences, tracing its roots to ancient Babylon, Egypt, and Greece. The philosopher and mathematician Pythagoras (569–490 BCE) is credited with formalising numerology in the Western tradition, teaching that numbers are the fundamental building blocks of the universe and that each carries a unique vibrational essence.

**How Numerology Works**

Every number from 1 to 9 (and the Master Numbers 11, 22, and 33) vibrates at a specific frequency that influences personality, life events, and spiritual evolution. By reducing larger numbers through digit-summing — a process called "reduction" — numerologists distil complex data (like a full birthdate or a name) into a single archetypal vibration.

**The Core Numbers Explained**

- **Life Path Number**: Derived from your birth date, this is your cosmic fingerprint — the overarching theme of your incarnation.
- **Expression Number**: Calculated from all letters of your full birth name, it reveals the talents and abilities you came to express.
- **Soul Urge Number**: Drawn from the vowels of your name, it speaks to the deepest longings of your soul — what you truly crave at a heart level.
- **Personality Number**: Formed by the consonants of your name, it shows the mask you wear in the world and how others first perceive you.

**Master Numbers**

11, 22, and 33 are considered Master Numbers — they carry amplified energy and a higher spiritual calling. Those with Master Numbers in their charts often feel a profound sense of purpose, along with greater challenges as the universe calls them to rise to their potential.

Numerology, like tarot, is best understood as a mirror — not a cage. Your numbers illuminate tendencies and potentials; your free will writes the story.
""")

# ── Additional section with internal and external links ─────────────────────
st.markdown("## The Legitimacy of Tarot: A Psychological Perspective")
st.write("""
Tarot cards have long been revered as more than mere tools of divination; they are profound instruments for introspection and self-discovery. Drawing upon the depth psychology of Carl Jung, tarot embodies the archetypal symbols that reside within the collective unconscious, mirroring the universal themes and inner conflicts that define the human experience.

Jung posited that archetypes are innate, universal prototypes for ideas and may be used to interpret observations. Each tarot card represents these archetypal energies, serving as a bridge between the conscious mind and the deeper layers of the psyche. When individuals engage with tarot, they tap into these universal symbols, allowing for a dialogue between their personal narratives and the broader human condition.

In the context of psychoanalysis, tarot functions as a reflective tool that facilitates the exploration of the subconscious. The imagery and symbolism of the cards encourage individuals to project their inner thoughts and emotions, unveiling patterns and motifs that might otherwise remain hidden. This process aligns with therapeutic practices that seek to bring unconscious material to light, promoting greater self-awareness and emotional healing.

Moreover, the structured yet flexible nature of tarot spreads provides a framework for individuals to navigate complex psychological landscapes. By interpreting the cards in relation to specific questions or life situations, users can gain insights into their motivations, fears, and aspirations. This reflective practice fosters a deeper understanding of oneself, empowering individuals to make informed decisions and embrace personal growth.

In essence, the legitimacy of tarot is anchored in its ability to resonate with the fundamental aspects of human psychology. By integrating Jungian archetypes and psychoanalytic principles, tarot offers a meaningful and transformative avenue for individuals to explore their inner worlds and cultivate a more profound connection with their authentic selves.
""")
st.markdown("[Learn More About Tarot's Psychological Roots](/about-tarot)")  # Internal link
st.markdown("[Explore Jungian Archetypes in Tarot](https://labyrinthos.co/blogs/learn-tarot-with-labyrinthos-academy/carl-jung-and-jungian-archetypes-in-the-tarot-the-various-aspects-of-our-selves?srsltid=AfmBOoqgyY0Ur-zwvlAWvccRlt_06NbCCfP_1okEg-2r6NONgtCGb3Mf)")  # External link to a reputable source
