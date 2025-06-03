# movie_therapy.py
import streamlit as st
import sys
import os
import ast 
import random
import time
import base64

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.recommender.cineclash import suggest_movies, compare_movies

def render():
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


    img_path = "assets/therbg.jpg"
    with open(img_path, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode()

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
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(""" 
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pacifico&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Comfortaa:wght@400;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;700&display=swap');
    div.stButton > button {
     display: block;
     margin-left: auto;
     margin-right: auto;
    }
    /* Global font */
    body, h2, h3, h4, h5, h6, p, span, div {
     font-family: 'Comfortaa', sans-serif !important;
     color: white;
    }

    /* Main title */
    .main-title, h1 {
     font-family: 'Pacifico', cursive !important;
     font-size: 3.5em;
     font-weight: 800;
     color: #C0C0C0;
     text-shadow: 0 0 10px #C0C0C0, 0 0 20px #D3D3D3, 0 0 30px #E0E0E0;
     animation: neonGlowSilver 2.5s ease-in-out infinite alternate;
     margin-bottom: 30px;
    }

    @keyframes neonGlowSilver {
     0% {
        text-shadow:
            0 0 5px #C0C0C0,
            0 0 10px #D3D3D3,
            0 0 20px #E0E0E0;
        opacity: 1;
     }
     50% {
        text-shadow:
            0 0 10px #C0C0C0,
            0 0 20px #D3D3D3,
            0 0 30px #E0E0E0;
        opacity: 0.9;
     }
     100% {
        text-shadow:
            0 0 5px #C0C0C0,
            0 0 10px #D3D3D3,
            0 0 20px #E0E0E0;
        opacity: 1;
     }
    }

    /* Section title */
    .section-title {
     font-size: 2.5em;
     font-weight: 700;
     margin-top: 40px;
     margin-bottom: 20px;
     color: #C0C0C0;
     text-shadow: 0 0 10px #C0C0C0, 0 0 30px #D3D3D3;
     animation: flickerSilver 3s infinite alternate;
     font-family: 'Pacifico', cursive !important;
    }

    @keyframes flickerSilver {
     0% { opacity: 1; text-shadow: 0 0 5px #C0C0C0, 0 0 10px #D3D3D3; }
     50% { opacity: 0.8; text-shadow: 0 0 15px #C0C0C0, 0 0 25px #D3D3D3; }
     100% { opacity: 1; text-shadow: 0 0 10px #C0C0C0, 0 0 30px #D3D3D3; }
    }

    /* Card Styles */

    .flip-card {
     background-color: transparent;
     width: 200px;
     height: 360px;
     perspective: 1000px;
     display: inline-block;
     margin: 1rem 0.75rem;
     animation: fadeIn 1.5s ease;
     font-family: 'Comfortaa', sans-serif !important;
     transition: transform 0.4s ease-in-out, box-shadow 0.4s ease;
    }

    .flip-card:hover {
     transform: scale(1.05);
    
    }

    .flip-card-inner {
     position: relative;
     width: 100%;
     height: 100%;
     text-align: center;
     transition: transform 0.8s ease-in-out;
     transform-style: preserve-3d;
    }

    .flip-card:hover .flip-card-inner {
     transform: rotateY(180deg);
    }

    .flip-card-front, .flip-card-back {
     position: absolute;
     width: 100%;
     height: 100%;
     border: 2px solid #999;
     backface-visibility: hidden;
     border-radius: 1rem;
     padding: 0.75rem;
     box-shadow: 0 0 10px #E0E0E0;
     overflow-wrap: break-word;
     word-break: break-word;
     line-height: 1.35;
     font-size: 0.87rem;
     overflow: auto;
     text-overflow: ellipsis;
    }

    .flip-card-back::after {
     content: "";
     position: absolute;
     bottom: 0;
     height: 20px;
     width: 100%;
     background: linear-gradient(to top, #1f2937, transparent);
     pointer-events: none;
    }

    .flip-card-front {
     background-color: #2F2F2F;  /* dark silver */
     color: #EEE !important
     overflow-y: auto;
    }

    .flip-card-back {
     background-color: #3A3A3A;  /* darker silver */
     color: #EEE !important;
     transform: rotateY(180deg);
     overflow-y: auto;
    } 

    .flip-card strong {
     color: #22D3EE;
    }

    .selected-card {
     border-color: #9b59b6 !important;
     box-shadow: 0 0 20px #9b59b6 !important;
     animation: shake 0.5s infinite alternate;
    } 

    @keyframes shake {
     0% { transform: rotate(0deg); }
     25% { transform: rotate(1deg); }
     50% { transform: rotate(-1deg); }
     75% { transform: rotate(1deg); }
     100% { transform: rotate(0deg); }
    }

    .select-button {
     margin-top: 0.5rem;
     background-color: #9b59b6;
     color: white;
     padding: 6px 12px;
     border-radius: 0.5rem;
     border: none;
     cursor: pointer;
     font-size: 0.9rem;
    }

    .select-button:hover {
     background-color: #8e44ad;
    }

    /* Selectbox animation (Streamlit select uses data-baseweb attr) */
    div[data-baseweb="select"] {
     transition: all 0.3s ease;
     border-radius: 10px !important;
     box-shadow: 0 0 5px #22D3EE55;
    }

    div[data-baseweb="select"]:hover {
     transform: scale(1.01);
     box-shadow: 0 0 12px #22D3EE, 0 0 20px #06B6D4;
    }

    /* CineClash Specific Styling */
    .cineclash-section * {
     font-family: 'Baloo 2', cursive !important;
    }

    /* Fade-in animation */
    @keyframes fadeIn {
     0% { opacity: 0; transform: translateY(20px); }
     100% { opacity: 1; transform: translateY(0); }
    }
    /* Override default button style */
    button[kind="primary"], div.stButton > button {
     font-family: 'Baloo 2', cursive !important;
     font-size: 1.1em;
     border-radius: 10px;
     background: linear-gradient(to right, #FF0080, #7928CA);
     color: white;
     border: none;
     padding: 0.6rem 1.2rem;
     box-shadow: 0 0 12px #FF80ABAA;
     transition: transform 0.2s ease;
    }

    div.stButton > button:hover {
     transform: scale(1.05);
     box-shadow: 0 0 15px #FF80AB, 0 0 25px #E040FB;
    }

    .cineclash-btn {
     font-size: 30px;
     border: none;
     border-radius: 12px;
     padding: 12px 35px;
     background: linear-gradient(to right, #f00, #f90, #ff0);
     color: black;
     cursor: pointer;
     animation: shake 0.7s infinite;
     box-shadow: 0 0 10px rgba(255,0,0,0.5);
     display: block;
     margin: 30px auto;
     width: 250px;
     font-weight: bold;
    }
    .retake-btn {
     font-size: 20px;
     border: none;
     border-radius: 10px;
     padding: 10px 25px;
     background: linear-gradient(to right, #ff8c00, #ffc107);
     color: black;
     cursor: pointer;
     animation: bounce 1.2s infinite;
     box-shadow: 0 0 8px rgba(255,140,0,0.7);
     display: block;
     margin: 20px auto;
     width: 200px;
     font-weight: bold;
    }
    @keyframes shake {
     0% { transform: translate(1px, 1px) rotate(0deg); }
     25% { transform: translate(-1px, 2px) rotate(-1deg); }
     50% { transform: translate(-3px, 0px) rotate(1deg); }
     75% { transform: translate(3px, 2px) rotate(0deg); }
     100% { transform: translate(1px, -2px) rotate(-1deg); }
    } 
    @keyframes bounce {
     0%, 100% { transform: translateY(0); }
     50% { transform: translateY(-5px); }
    }
    .clash-header {
     font-size: 45px;
     text-align: center;
     font-weight: bold;
     animation: fadeIn 1.5s ease-in-out;
     margin-bottom: 30px;
    }
    @keyframes fadeIn {
     0% { opacity: 0; transform: scale(0.8); }
     100% { opacity: 1; transform: scale(1); }
    }
    .popcorn-burst {
     animation: burst 1s ease-in-out infinite alternate;
     font-size: 40px;
     display: inline-block;
     margin: 0 8px;
    }
    @keyframes burst {
     0% { transform: scale(1) translateY(0); opacity: 1; }
     100% { transform: scale(1.3) translateY(-10px); opacity: 0.7; }
    }
    .thermometer-horizontal {
     height: 20px;
     background: #eee;
     border-radius: 15px;
     margin: 20px auto;
     position: relative;
     box-shadow: inset 0 0 5px #ccc;
    }
    .thermometer-fill {
     height: 100%;
     background: linear-gradient(to right, #f00, #f90, #ff0);
     border-radius: 15px;
     animation: fillWidth 3s ease forwards;
    }
    .param-table {
     width: 90%;
     margin: 0 auto 30px;
     border-collapse: collapse;
    }
    .param-table th, .param-table td {
     border: 1px solid #ddd;
     padding: 10px 15px;
     text-align: center;
    }
    .param-table th {
     background-color: #ffcc00;
     color: #000;
     font-weight: 600;
    }
    .param-title {
     font-weight: bold;
     background-color: #ffeb99;
    }
    .centered-button-container {
     display: flex;
     justify-content: center;
     margin-top: 20px;
     margin-bottom: 20px;
    }
    .stButton > button {
     background-color: #FFA500 !important;  /* Soft orange */
     color: white !important;
     font-weight: bold;
     padding: 10px 25px;
     border-radius: 12px;
     border: none;
     font-size: 16px;
     box-shadow: 0 4px 6px rgba(0,0,0,0.1);
     transition: transform 0.2s ease, box-shadow 0.2s ease;
     position: relative;
     overflow: hidden;
    }

    /* Hover effects */
     .stButton > button:hover {
     transform: scale(1.05);
     box-shadow: 0 6px 12px rgba(0,0,0,0.2);
    }

    /* Text shimmer effect */
    .stButton > button::after {
     content: '';
     position: absolute;
     top: 0;
     left: -75%;
     width: 50%;
     height: 100%;
     background: linear-gradient(120deg, rgba(255,255,255,0.1), rgba(255,255,255,0.4), rgba(255,255,255,0.1));
     transform: skewX(-25deg);
    }

    /* Animate the shimmer on hover */
    .stButton > button:hover::after {
     animation: shimmer 1.5s infinite;
    }

    @keyframes shimmer {
     0% { left: -75%; }
     100% { left: 125%; }
    }

    @media screen and (max-width: 768px) {
     .flip-card {
         width: 90% !important;
         margin: 1rem auto !important;
     }
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("Mood-Based Movie Therapy")

    mood = st.selectbox("Pick your mood:", [
        "Happy / Cheerful", "Sad / Heartbroken", "Angry / Frustrated",
        "Anxious / Overwhelmed", "Bored / Restless", "Romantic / Dreamy",
        "Curious / Thoughtful", "Lonely / Nostalgic",
        "Playful / Mischievous", "Inspired / Motivated"
    ])

    if st.button("Suggest Movies🎥"):
        suggested = suggest_movies(mood)
        st.session_state.suggested = suggested
        st.session_state.selected = []
    if "suggested" in st.session_state:
        st.subheader("Your Movie Therapy Dose:")
        cols = st.columns(5)
        for i, movie in enumerate(st.session_state.suggested.itertuples()):
           selected = movie.title in st.session_state.selected
           card_class = "flip-card selected-card" if selected else "flip-card"
           with cols[i]:
              st.markdown(f"""
              <div class="{card_class}">
                  <div class="flip-card-inner">
                      <div class="flip-card-front">
                        <h4>{movie.title}</h4>
                        <p>⏱ {movie.runtime} mins</p>
                        <p>🎬 {movie.director}</p>
                        <p>🎭 {', '.join(eval(movie.cast)[:5])}</p>
                        <p>📚 {movie.genres}</p>
                        <p>🈹 {movie.language}</p>
                      </div>
                      <div class="flip-card-back">
                        <p>{movie.description}</p>
                      </div>
                  </div>
              </div>
              """, unsafe_allow_html=True)

              if st.button(f"Select {i+1}", key=f"select_{i}"):
                  if movie.title not in st.session_state.selected and len(st.session_state.selected) < 2:
                     st.session_state.selected.append(movie.title)


    if "show_cineclash" not in st.session_state:
        st.session_state.show_cineclash = False

    if len(st.session_state.get("selected", [])) == 2:
        if not st.session_state.show_cineclash:
            with st.container():
                st.markdown('<div class="centered-button-container">', unsafe_allow_html=True)
                if st.button("⚔️ CineClash!", key="cineclash_btn"):
                    st.session_state.show_cineclash = True
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="clash-header">🎮CineClash Arena🎮</div>', unsafe_allow_html=True)
            with st.spinner("Loading battle stats..."):
                time.sleep(1.5)

            stats1, stats2, score1, score2 = compare_movies(
                st.session_state.selected[0], 
                st.session_state.selected[1]
            )

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"### {stats1['title']}")
                for key, val in stats1.items():
                    if key != "title":
                        st.write(f"**{key.replace('_', ' ').title()}:** {val}")
            with col2:
                st.markdown(f"### {stats2['title']}")
                for key, val in stats2.items():
                    if key != "title":
                        st.write(f"**{key.replace('_', ' ').title()}:** {val}")

            winner = stats1["title"] if score1 > score2 else stats2["title"]
            st.markdown(f"""
            <div style="text-align:center; margin-top: 30px;">
                <h3>The winner is: <strong>{winner}</strong>! 🎉</h3>
                <div>
                    <span class="popcorn-burst">🍿</span>
                    <span class="popcorn-burst">🍿</span>
                    <span class="popcorn-burst">🍿</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            fill_percent = int(max(score1, score2) / 6 * 100)
            st.markdown(f"<p style='text-align:center'><b>🔥 Score: {max(score1, score2)} / 6</b></p>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="thermometer-horizontal">
                <div class="thermometer-fill" style="width: {fill_percent}%;"></div>
            </div>
            """, unsafe_allow_html=True)

            with st.container():
                st.markdown('<div class="centered-button-container">', unsafe_allow_html=True)
                if st.button("🔁 Retake CineClash", key="retake_btn"):
                    st.session_state.selected = []
                    st.session_state.show_cineclash = False
                    st.rerun()
                st.markdown("""
                <p style='text-align:center; font-size:16px; margin-top: 10px;'>👉 Please click on the Retake button to clash other movies!</p>
                """, unsafe_allow_html=True)
    else:
        st.info("Please double click on the select button and select exactly 2 movies to enable CineClash")
