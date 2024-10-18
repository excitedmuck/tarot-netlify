import streamlit as st
import random
import openai
from datetime import datetime
import os

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

# Streamlit app
st.title("✨ Mystical Tarot de Multiverse ✨")

# Sidebar for PayPal``
st.sidebar.title("Support the Creator")
st.sidebar.write("I'm a free bird in autopoeisis poetry of code and word, I'm passionate about earth observation in deed and word, I like helping you get answers truly absurd.")
st.sidebar.write("I'm trying to raise butterfly wings for my cacoon. If this app has helped you in any way, buy me a molly and give me a hug!")
st.sidebar.markdown("[Bestow Me a Molly](https://buymeacoffee.com/yashvinishz)")
st.sidebar.write("Your love means the world to me. So may you never run out of molly! 🥰😉")


# Get the user's question
question = st.text_input("🔮 Whisper your question to the cosmos...")

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

# Let the user choose the spread type
spread_type = st.selectbox("Choose your cosmic spread:", list(spread_types.keys()))

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
        st.subheader("🌌 Cosmic Interpretation 🌌")
        
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
