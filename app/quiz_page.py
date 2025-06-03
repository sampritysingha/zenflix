import streamlit as st
import sys
import os
import random
import base64

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.personality_matcher.personality_quiz import run_personality_quiz

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

    img_path = "assets/quizbg.jpg"
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

    # --- Custom CSS Styling ---
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Fugaz+One&family=Share+Tech+Mono&family=Cinzel+Decorative:wght@700&display=swap');

            html, body, [class*="css"] {
                font-family: 'Share Tech Mono', monospace;
                background-color: #111827;
                color: #ffffff;
            }

            h1 {
                font-family: 'Cinzel Decorative', cursive;
                font-size: 3em;
                text-shadow: 2px 2px 4px rgba(255, 0, 0, 0.8);
                animation: glowTitle 2s ease-in-out infinite alternate;
            }

            @keyframes glowTitle {
                from { text-shadow: 0 0 5px #ff0000, 0 0 10px #ff4444, 0 0 15px #ff8888; }
                to { text-shadow: 0 0 20px #ff3333, 0 0 30px #ff6666, 0 0 40px #ff9999; }
            }

            .question-card {
                background: rgba(0, 0, 0, 0.75);
                padding: 30px;
                border-radius: 20px;
                box-shadow: 0 0 30px rgba(255, 255, 255, 0.3);
                margin-bottom: 20px;
                animation: fadeSlideIn 0.6s ease-in-out;
            }

            @keyframes fadeSlideIn {
                0% { opacity: 0; transform: translateY(20px); }
                100% { opacity: 1; transform: translateY(0); }
            }

            div[role="radiogroup"] > div {
                background-color: #1e1e1e;
                border: 2px solid #fcd34d;
                border-radius: 15px;
                margin-bottom: 15px;
                padding: 20px 25px;
                cursor: pointer;
                transition: all 0.3s ease;
                user-select: none;
            }

            div[role="radiogroup"] > div:hover {
                background-color: #fde68a22;
                box-shadow: 0 0 15px #facc15;
                transform: scale(1.03);
            }

            div[role="radiogroup"] > div[aria-checked="true"] {
                background-color: #facc15;
                color: black;
                font-weight: bold;
                box-shadow: 0 0 25px #facc15;
            }

            input[type="radio"] {
                display: none;
            }

            .progress-bar {
                height: 10px;
                background: linear-gradient(to right, #facc15, #f59e0b);
                border-radius: 20px;
                margin-top: 20px;
                transition: width 0.4s ease;
            }

            .flip-card {
                background-color: transparent;
                width: 100%;
                max-width: 500px;
                height: 400px;
                perspective: 1000px;
                margin: auto;
                position: relative;
                z-index: 1;
                animation: float 3s ease-in-out infinite;
                box-shadow: 0 0 20px 5px red;
                border-radius: 20px;
            }
            @keyframes float {
               0%   { transform: translateY(0px); }
               50%  { transform: translateY(-15px); }
               100% { transform: translateY(0px); }
            }
            .flip-card-inner {
              position: relative;
              width: 100%;
              height: 100%;
              transition: transform 1s;
              transform-style: preserve-3d;
            }

            .flip-card:hover .flip-card-inner {
                transform: rotateY(180deg);
            }

            .flip-card-front, .flip-card-back {
               position: absolute;
               width: 100%;
               height: 100%;
               backface-visibility: hidden;
               border-radius: 20px;
               overflow: hidden;
               display: flex;
               flex-direction: column;
               justify-content: center;
               align-items: center;
            }

            .flip-card-front {
               background-color: #111;
               color: white;
            }

            .flip-card-back {
               background-color: #1f1f1f;
               color: white;
               transform: rotateY(180deg);
            }

            
            h2, h3, p, strong {
                font-family: 'Share Tech Mono', monospace;
            }
                
            div.stButton > button#retake_button {
             background-color: #ff1a1a;
             color: white;
             border: none;
             padding: 12px 24px;
             border-radius: 50px;
             box-shadow: 0 0 10px #ff1a1a, 0 0 20px #ff1a1a;
             font-size: 18px;
             font-weight: bold;
             transition: all 0.3s ease;
             position: relative;
             z-index: 1;
            }

            div.stButton > button#retake_button:hover {
             background-color: #ff4d4d;
             box-shadow: 0 0 15px #ff1a1a, 0 0 30px #ff3333, 0 0 40px #ff6666;
             cursor: pointer;
            }

            /* Optional: Sparkle effect */
             div.stButton > button#retake_button::after {
             content: "✨";
             position: absolute;
             top: -10px;
             right: -10px;
             animation: sparkle 2s infinite linear;
            }

            @keyframes sparkle {
             0% { opacity: 1; transform: scale(1) rotate(0deg); }
             50% { opacity: 0.3; transform: scale(1.5) rotate(180deg); }
             100% { opacity: 1; transform: scale(1) rotate(360deg); }
            }
        </style>
                
    """, unsafe_allow_html=True)

    st.markdown("""
    <h1 style='text-align: center;'>🍿 Which Movie Are You?</h1>
    <p style='text-align: center;'>Unravel your cinema soul with this fun quiz! 🎭🎬</p>
    """, unsafe_allow_html=True)

    all_questions = [
        ("What kind of day are you having?", [
            "A chaotic adventure with unexpected turns",
            "A slow rainy vibe with deep thoughts",
            "High energy, non-stop fun",
            "Calm and introspective, like a poem"]),
        ("Which setting feels more like 'you'?", [
            "An 80s neon-lit city",
            "A medieval castle under siege",
            "An indie cafe on a rainy day",
            "A post-apocalyptic desert highway"]),
        ("Pick a soundtrack for your life:", [
            "Epic orchestral score",
            "Lo-fi beats with ambient rain",
            "Fast techno or EDM",
            "Haunting piano melody"]),
        ("Choose your ideal sidekick:", [
            "A loyal robot with a heart",
            "A mysterious stranger with a past",
            "A talking animal with sass",
            "No sidekick—I’m a lone wolf"]),
        ("Which quote speaks to your soul?", [
            "Carpe diem, baby!",
            "Even in the dark, we bloom",
            "Chaos is the natural order",
            "Stories live longer than people"]),
        ("What’s your cinematic guilty pleasure?", [
            "Over-the-top musical numbers",
            "Melodramatic monologues",
            "Cheesy horror jump scares",
            "Romantic slow-motion spins"]),
        ("How do you handle surprises?", [
            "Bring it on!",
            "I overthink then act",
            "Laugh it off",
            "Run the other way"]),
        ("Pick your aesthetic:", [
            "Vintage film grain",
            "Hypercolor Y2K",
            "Rustic realism",
            "Dreamy surrealism"]),
        ("Who are you at a party?", [
            "The mysterious observer",
            "The chaos creator",
            "The playlist master",
            "The soul who starts deep convos"]),
        ("What drives your decisions?", [
            "Intuition",
            "Logic",
            "Emotion",
            "Curiosity"])
    ]

    if 'step' not in st.session_state:
        st.session_state.step = 0
        st.session_state.answers = []
        st.session_state.selected_qs = random.sample(all_questions, 5)

    if st.session_state.step < 5:
        current_q, current_opts = st.session_state.selected_qs[st.session_state.step]

        with st.container():
            st.markdown(f"""
                <div class="question-card">
                    <h3>Q{st.session_state.step + 1}: {current_q}</h3>
                </div>
            """, unsafe_allow_html=True)

        selected_key = f"q{st.session_state.step+1}_selected"
        if selected_key not in st.session_state:
            st.session_state[selected_key] = None

        st.session_state[selected_key] = st.radio(
            "👇 Choose your vibe:", current_opts,
            index=current_opts.index(st.session_state[selected_key]) if st.session_state[selected_key] in current_opts else 0,
            key=f"q{st.session_state.step+1}",
            label_visibility="collapsed"
        )

        progress_percent = int(((st.session_state.step + 1) / 5) * 100)
        st.markdown(f"**Progress: {progress_percent}%**")
        st.markdown(f"""<div class='progress-bar' style='width: {progress_percent}%;'></div>""", unsafe_allow_html=True)

        if st.button("Next", disabled=(st.session_state[selected_key] is None)):
            if len(st.session_state.answers) == st.session_state.step:
                selected_index = current_opts.index(st.session_state[selected_key]) + 1
                st.session_state.answers.append(selected_index)
                st.session_state.step += 1
                next_key = f"q{st.session_state.step+1}_selected"
                if next_key in st.session_state:
                    del st.session_state[next_key]
            st.rerun()

    else:
        with st.spinner("🎞️ Rolling film reels... finding your cinematic soulmate..."):
            result = run_personality_quiz(st.session_state.answers)

        st.balloons()
        st.markdown("## 🍿 Your Movie Match Is In...")

        st.markdown(f"""
            <div class="flip-card">
              <div class="flip-card-inner">
                <div class="flip-card-front">
                  <h2>{result['🎬 You are...']}</h2>
                  <p>🎭 <strong>Genre:</strong> {result['Genres']}</p>
                  <p>🎬 <strong>Director:</strong> {result['Director']}</p>
                  <p>🌍 <strong>Language:</strong> {result['Language']}</p>
                  <p>⭐ <strong>Rating:</strong> {result['Rating']}</p>
                  <p>🧑‍🤝‍🧑 <strong>Cast:</strong> {', '.join(str(c).strip("[]'\"") for c in result['Cast'][:5])}</p>
                </div>
                <div class="flip-card-back">
                  <p><strong>📖 Plot:</strong> {result['📖 Description']}</p>
                  <p><strong>🌡 Sentiment Match Score:</strong> {result['🌡 Sentiment Match Score']}</p>
                </div>
              </div>
            </div>
        """, unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
           if st.button("🔁 Retake Quiz", key="retake_button"):
              for key in ['step', 'answers'] + [f'q{i}_selected' for i in range(1, 6)]:
                 if key in st.session_state:
                   del st.session_state[key]
              st.rerun()



