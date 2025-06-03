# app/zodiac_app.py

import streamlit as st
import pandas as pd
import base64
import sys
import os

# Add path to src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.zodiac.zodiac_generator import assign_zodiac_roles, load_movie_data

def render():
    df = load_movie_data()

    img_path = "assets\night.jpg"
    with open(img_path, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode()
        
    col1, col2 = st.columns([1, 6])
    with col1:
      st.markdown(
        """
        <a href="?page=home" style="text-decoration: none;">
            <button style="
                width: 50px;
                height: 50px;
                border-radius: 50%;
                background-color: white;
                color: black;
                border: none;
                cursor: pointer;
                font-size: 22px;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 0 12px rgba(255, 255, 255, 0.7), 0 0 24px rgba(255, 255, 255, 0.5);
                transition: all 0.3s ease;
            ">
                🏠
            </button>
        </a>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{img_base64}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
            min-height: 100vh;
        }}

        .main, section[data-testid="stAppViewContainer"] {{
            background-color: transparent !important;
        }}

        .main .block-container {{
            background-color: rgba(0, 0, 0, 0.5);
            border-radius: 15px;
            padding: 2rem;
            backdrop-filter: blur(5px);
        }}

        h1, h2, h3, p, label, li {{
            color: #FFD700 !important;
            text-shadow: 0 0 10px #FFD700;
        }}

        @keyframes twinkle {{
            0%, 100% {{ opacity: 0.8; }}
            50% {{ opacity: 0.2; }}
        }}

        @keyframes float {{
            0% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-8px); }}
            100% {{ transform: translateY(0px); }}
        }}

        .star {{
            position: fixed;
            width: 2px;
            height: 2px;
            background: #fff;
            border-radius: 50%;
            animation: twinkle 2s infinite ease-in-out;
        }}

        .star:nth-child(2n) {{ animation-delay: 1s; }}
        .star:nth-child(3n) {{ animation-delay: 1.5s; }}

        .tarot-card {{
            background: rgba(255, 215, 0, 0.07);
            border: 1px solid rgba(255, 215, 0, 0.4);
            border-radius: 1rem;
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            color: white;
            padding: 1rem;
            margin: 1rem;
            position: relative;
            overflow: hidden;
            animation: float 4s ease-in-out infinite;
            transition: transform 0.4s ease, box-shadow 0.4s ease, background 0.4s ease;
            box-shadow: 0 0 30px rgba(255, 215, 0, 0.5), 0 0 60px rgba(255, 215, 0, 0.3);
            font-family: 'Montserrat', sans-serif !important;
        }}

        .tarot-card:hover {{
            transform: scale(1.05);
            background: rgba(255, 215, 0, 0.12);
            box-shadow: 0 0 50px rgba(255, 215, 0, 0.9), 0 0 90px rgba(255, 215, 0, 0.5);
        }}

        .tarot-card::before {{
            content: "";
            position: absolute;
            top: 0;
            left: -75%;
            width: 50%;
            height: 100%;
            background: linear-gradient(
                120deg,
                transparent 0%,
                rgba(255, 255, 255, 0.25) 50%,
                transparent 100%
            );
            transform: skewX(-25deg);
            animation: shimmer 2.5s infinite;
            pointer-events: none;
            z-index: 1;
        }}

        .tarot-card > * {{
            position: relative;
            z-index: 2;
        }}

        @keyframes shimmer {{
            0% {{ left: -75%; }}
            100% {{ left: 125%; }}
        }}
        </style>

        <script>
        const stars = 60;
        for (let i = 0; i < stars; i++) {{
            const star = document.createElement('div');
            star.classList.add('star');
            star.style.top = `${{Math.random() * 100}}%`;
            star.style.left = `${{Math.random() * 100}}%`;
            document.body.appendChild(star);
        }}
        </script>
        """, unsafe_allow_html=True
    )

    # Title
    st.markdown("""
        <h1 style='text-align: center; font-size: 3.5rem;'>🔮 Discover Your Cinematic Zodiac 🔮</h1>
        <p style='text-align: center; font-size: 1.3rem;'>What do your favorite films say about your inner star map? Give us 3 movies which resonate with you!</p>
    """, unsafe_allow_html=True)
    st.markdown("---")

    with st.form("zodiac_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            sun_movie = st.text_input("🌞 Sun Movie (personal fav)", max_chars=50)
        with col2:
            moon_movie = st.text_input("🌙 Moon Movie (guilty pleasure)", max_chars=50)
        with col3:
            rising_movie = st.text_input("🌅 Rising Movie (crowd fav you agree with)", max_chars=50)

        submit = st.form_submit_button("Reveal My Zodiac Chart")

    def display_tarot_card(role, data):
        st.markdown(f"""
        <div class='tarot-card'>
            <h2>🃏 {role}</h2>
            <h3>{data['Zodiac Match']}</h3>
            <p><i>{data['Zodiac Role']}</i></p>
            <ul>
                <li><b>Genre Similarity:</b> {data['Genre Similarity']}</li>
                <li><b>Sentiment Score:</b> {data['Sentiment Polarity Score']}</li>
                <li><b>Director:</b> {data['Director']}</li>
                <li><b>Genres:</b> {data['Genre']}</li>
            </ul>
            <p><b>Reasoning:</b><br>{data['Reason for Genre Similarity']}<br>{data['Reason for Sentiment Match']}</p>
            <p>{data['Description']}</p>
        </div>
        """, unsafe_allow_html=True)

    if submit:
        user_movies = [sun_movie.strip().title(), moon_movie.strip().title(), rising_movie.strip().title()]
        zodiac_chart = assign_zodiac_roles(df, user_movies)

        st.balloons()
        st.markdown("<h2 style='text-align: center;'>✨ Your Cinematic Zodiac ✨</h2>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        for role, col in zip(['Sun', 'Moon', 'Rising'], [col1, col2, col3]):
            with col:
                if isinstance(zodiac_chart[role], dict):
                    display_tarot_card(role, zodiac_chart[role])
                else:
                    st.error(zodiac_chart[role])
