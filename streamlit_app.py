import streamlit as st  
import json
import base64

st.set_page_config(page_title="Zenflix", page_icon="🍿", layout="wide")
# Convert image to base64
def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Load assets
bucket_base64 = get_base64_image("assets/bucket.png")
title_img_base64 = get_base64_image("assets/title.png")

popcorn_buttons = [
    {"label": "Movie Therapy", "img": "assets/popcorn1.png", "target": "therapy", "class": "popcorn1"},
    {"label": "Leaderboards", "img": "assets/popcorn2.png", "target": "leaderboards", "class": "popcorn2"},
    {"label": "Which Movie Are You?", "img": "assets/popcorn3.png", "target": "whichmovie", "class": "popcorn3"},
    {"label": "Cinematic Zodiac", "img": "assets/popcorn4.png", "target": "zodiac", "class": "popcorn4"},
]

# Load animated background
gif_path = "assets/film.gif"
with open(gif_path, "rb") as f:
    gif_base64 = base64.b64encode(f.read()).decode("utf-8")

# Background and base styles
st.markdown(
    f"""
    <style>
    .stApp {{
        background: url("data:image/gif;base64,{gif_base64}") no-repeat center center fixed;
        background-size: cover;
    }}
    section[data-testid="stAppViewContainer"] {{
        background-color: rgba(0, 0, 0, 0.5) !important;
    }}

    @keyframes bounce {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-12px); }}
    }}

    @keyframes pulse {{
        0%, 100% {{ transform: scale(1); }}
        50% {{ transform: scale(1.05); }}
    }}

    .bucket-img {{
        width: 350px;
        animation: bounce 2s infinite;
        margin-bottom: -140px;
    }}

    .title-img {{
        animation: pulse 4s ease-in-out infinite;
        width: 100%;
        max-width: 500px;
        height: auto;
        margin-bottom: 20px;
    }}

    .popcorn-button {{
        position: absolute;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        cursor: pointer;
        z-index: 2;
        animation: bounce 2s infinite;
    }}

    .popcorn-button img {{
        width: 95px;
        height: auto;
        border-radius: 12px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.2);
        transition: transform 0.3s ease, filter 0.3s ease;
    }}

    .popcorn-button:hover img {{
        transform: scale(1.1) rotate(-3deg);
        filter: drop-shadow(0 0 12px rgba(255, 223, 70, 0.9));
    }}

    .popcorn-label {{
        margin-bottom: 6px;
        font-weight: bold;
        font-size: 0.75em;
        color: white;
        text-shadow: 2px 2px 5px black;
        background: rgba(0,0,0,0.4);
        padding: 3px 8px;
        border-radius: 6px;
    }}

    /* Exact positions for larger screens */
    .popcorn1 {{ top: -35px; left: -10px; }}
    .popcorn2 {{ top: -90px; left: 85px; }}
    .popcorn3 {{ top: -125px; left: 175px; }}
    .popcorn4 {{ top: -85px; left: 270px; }}

    .title-container {{
        margin-top: 80px;
        padding-left: 40px;
    }}

    @media screen and (max-width: 768px) {{
        .st-emotion-cache-z5fcl4 {{
            flex-direction: column-reverse !important;
        }}
        .title-container {{
            margin-top: 40px;
            padding-left: 0;
            text-align: center;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ROUTING
query_params = st.query_params
page = query_params.get("page", "home")

if page == "home":
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.markdown("<div style='position:relative; margin-top:100px;'>", unsafe_allow_html=True)
        for btn in popcorn_buttons:
            img_base64 = get_base64_image(btn["img"])
            target_url = f"/?page={btn['target']}"
            st.markdown(f"""
                <a href="{target_url}" class="popcorn-button {btn['class']}">
                    <div class="popcorn-label">{btn['label']}</div>
                    <img src="data:image/png;base64,{img_base64}" />
                </a>
            """, unsafe_allow_html=True)
        st.markdown(f"""
            <img src="data:image/png;base64,{bucket_base64}" class="bucket-img" />
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="title-container">
                <img src="data:image/png;base64,{title_img_base64}" class="title-img" />
        """, unsafe_allow_html=True)

        subtitle_img = get_base64_image("assets/subtitle1.png")
        st.markdown(f"""
            <div style="margin-top: 80px;">
                <img src="data:image/png;base64,{subtitle_img}" class="subtitle-img" />
            </div>
            </div>
        """, unsafe_allow_html=True)

elif page == "therapy":
    from app import movie_therapy
    movie_therapy.render()

elif page == "leaderboards":
    from app import leaderboard_page
    leaderboard_page.render()

elif page == "whichmovie":
    from app import quiz_page
    quiz_page.render()

elif page == "zodiac":
    from app import zodiac_page
    zodiac_page.render()

else:
    st.error("Page not found.")

# Footer
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600&display=swap" rel="stylesheet">
<style>
.scroll-footer {
    text-align: center;
    margin-top: 100px;
    font-family: 'Cormorant Garamond', serif;
    font-size: 22px;
    color: #FFD700;
    text-shadow: 0 0 10px #FFD700;
    animation: fadeIn 2s ease-in;
}
.scroll-footer a {
    color: #FFD700;
    text-decoration: none;
    margin: 0 12px;
    font-size: 18px;
    transition: 0.3s;
}
.scroll-footer a:hover {
    color: white;
    text-shadow: 0 0 6px #fff;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>

<div class="scroll-footer">
    Made with ❤️ • Zenflix 2025 <br>
    <a href="https://github.com/sampritysingha" target="_blank">GitHub</a> |
    <a href="https://www.linkedin.com/in/sampritysingha29" target="_blank">LinkedIn</a>
</div>
""", unsafe_allow_html=True)
