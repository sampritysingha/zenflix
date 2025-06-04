import streamlit as st 
import pandas as pd
import sys
import os
import ast 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.data_loader import load_movie_data, load_director_stats
from src.leaderboard.director_popularity import (
    get_top_directors,
    get_underrated_legends,
    get_most_prolific,
    get_most_viewed_directors,
    get_popular_and_critically_acclaimed,
    get_hidden_gems,
    get_top_movies_by_genre,
)

from src.leaderboard.actor_insights import (
    load_actor_stats,
    get_top_actors_by_rating,
    get_versatile_actors,
    get_most_liked_actors,
    get_most_frequent_collaborators
)
# === ✅ Caching Layer ===
@st.cache_data
def cached_load_director_stats():
    return load_director_stats()

@st.cache_data
def cached_load_movies_data():
    return load_movie_data()

@st.cache_data
def cached_load_actor_stats():
    return load_actor_stats()

@st.cache_data
def cached_get_top_directors(stats_df, movies_df):
    return get_top_directors(stats_df, movies_df)

@st.cache_data
def cached_get_underrated_legends(stats_df, movies_df):
    return get_underrated_legends(stats_df, movies_df)

@st.cache_data
def cached_get_most_prolific(stats_df, movies_df):
    return get_most_prolific(stats_df, movies_df)

@st.cache_data
def cached_get_most_viewed_directors(stats_df, movies_df):
    return get_most_viewed_directors(stats_df, movies_df)

@st.cache_data
def cached_get_popular_and_critically_acclaimed(stats_df, movies_df):
    return get_popular_and_critically_acclaimed(stats_df, movies_df)

@st.cache_data
def cached_get_hidden_gems(movies_df):
    return get_hidden_gems(movies_df)

@st.cache_data
def cached_get_top_movies_by_genre(movies_df, genre):
    return get_top_movies_by_genre(movies_df, genre)

@st.cache_data
def cached_get_top_actors_by_rating(actor_df):
    return get_top_actors_by_rating(actor_df)

@st.cache_data
def cached_get_versatile_actors(actor_df):
    return get_versatile_actors(actor_df)

@st.cache_data
def cached_get_most_liked_actors(actor_df):
    return get_most_liked_actors(actor_df)

@st.cache_data
def cached_get_most_frequent_collaborators(actor_df):
    return get_most_frequent_collaborators(actor_df)

# === UI Renderer ===
def render():
    st.title("🏆 Zenflix Leaderboards")
    st.markdown("<h1 style='color:#FBBF24;'>Zenflix Leaderboards🏆</h1>", unsafe_allow_html=True)

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

    # Load data
    stats_df = cached_load_director_stats()
    movies_df = cached_load_movies_data()

    if stats_df.empty or movies_df.empty:
        st.error("Could not load datasets. Please check the data paths.")
        st.stop()
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Poppins:wght@300;500;700&display=swap');

        /* Global font */
        body, h1, h2, h3, h4, h5, h6, p, span, div {
            font-family: 'Montserrat', 'Poppins', sans-serif !important;
            color: white;
        }

        /* Main title - change selector as needed */
        .main-title, h1 {
            font-family: 'Montserrat', sans-serif !important;
            font-size: 3.5em;
            font-weight: 800;
            color: #FFD700;
            text-shadow: 0 0 15px #FFD700, 0 0 30px #FFA500;
            animation: neonGlow 2.5s ease-in-out infinite alternate;
            margin-bottom: 30px;
        }

        @keyframes neonGlow {
            0% {
                text-shadow:
                    0 0 5px #FFD700,
                    0 0 10px #FFA500,
                    0 0 20px #FFD700,
                    0 0 30px #FFA500;
                opacity: 1;
            }
            50% {
                text-shadow:
                    0 0 10px #FFD700,
                    0 0 20px #FFA500,
                    0 0 30px #FFD700,
                    0 0 40px #FFA500;
                opacity: 0.9;
            }
            100% {
                text-shadow:
                    0 0 5px #FFD700,
                    0 0 10px #FFA500,
                    0 0 20px #FFD700,
                    0 0 30px #FFA500;
                opacity: 1;
            }
        }

        .section-title {
            font-size: 2.5em;
            font-weight: 700;
            margin-top: 40px;
            margin-bottom: 20px;
            color: #FFD700;
            text-shadow: 0 0 10px #FFD700, 0 0 30px #FFA500;
            animation: flicker 3s infinite alternate;
            font-family: 'Montserrat', sans-serif !important;
        }

        @keyframes flicker {
            0% { opacity: 1; text-shadow: 0 0 5px #FFD700, 0 0 10px #FFA500; }
            50% { opacity: 0.8; text-shadow: 0 0 15px #FFD700, 0 0 25px #FFA500; }
            100% { opacity: 1; text-shadow: 0 0 10px #FFD700, 0 0 30px #FFA500; }
        }

        .card {
         background: rgba(255, 215, 0, 0.08); /* translucent white */
         border-radius: 1rem;
         border: 1px solid rgba(255, 215, 0, 0.3);
         backdrop-filter: blur(10px); /* blur background behind */
         -webkit-backdrop-filter: blur(10px); /* for Safari */
         box-shadow: 0 0 15px rgba(255, 215, 0, 0.4);
         padding: 1rem;
         margin: 0.5rem;
         transition: transform 0.3s ease, box-shadow 0.3s ease;
         font-family: 'Montserrat', sans-serif !important;
         color: white; /* text color */
         position: relative;
        }

        .card:hover {
         transform: scale(1.05);
         box-shadow: 0 0 30px rgba(255, 215, 0, 0.8);
        }


        .card::after {
            content: "";
            position: absolute;
            top: 0; left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(120deg, transparent, rgba(255,255,255,0.05), transparent);
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.5s;
        }

        .card:hover::after {
            opacity: 1;
        }

        @keyframes floatCard {
            0% { transform: translateY(0); }
            50% { transform: translateY(-6px); }
            100% { transform: translateY(0); }
        }

        .flip-card {
            background-color: transparent;
            width: 260px;
            height: 340px;
            perspective: 1000px;
            display: inline-block;
            margin: 1rem;
            animation: fadeIn 1.5s ease;
            font-family: 'Montserrat', sans-serif !important;
        }

        .flip-card-inner {
            position: relative;
            width: 100%;
            height: 100%;
            text-align: center;
            transition: transform 0.8s;
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
            border-radius: 1rem;
            padding: 1rem;
            box-shadow: 0 0 15px #10B981;
        }

        .flip-card-front {
            background-color: #111827;
            color: white;
        }

        .flip-card-back {
            background-color: #1f2937;
            color: white;
            transform: rotateY(180deg);
            overflow-y: auto;
        }

        .flip-card strong {
            color: #22D3EE;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .genre-movie:hover {
            color: #FBBF24;
            transform: scale(1.05);
            transition: all 0.3s ease-in-out;
            text-shadow: 0 0 10px #FBBF24;
        }

        .highlight {
            color: #10B981;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { text-shadow: 0 0 5px #10B981; }
            50% { text-shadow: 0 0 15px #10B981; }
            100% { text-shadow: 0 0 5px #10B981; }
        }

        body, .stApp {
         background-image: radial-gradient(white 1px, transparent 1px), radial-gradient(white 1px, transparent 1px);
         background-position: 0 0, 25px 25px;
         background-size: 50px 50px;
         background-repeat: repeat;
         background-color: #111827; /* fallback background */
        }
    </style>

    """, unsafe_allow_html=True)

    st.markdown("<div class='section-title'>🌟 Director Highlights</div>", unsafe_allow_html=True)
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "⭐ Top Directors", "💎 Underrated Legends", "🎥 Most Prolific",
        "👀 Most Viewed", "🔥 Popular & Acclaimed"
    ])

    with tab1:
        top_directors = cached_get_top_directors(stats_df, movies_df)
        for _, row in top_directors.iterrows():
            st.markdown(f"<div class='card'><strong>🎬 {row['director']}</strong><br>Avg Rating: {row['avg_rating']:.2f}<br>Top Movies: <em>{row['top_movies']}</em></div>", unsafe_allow_html=True)

    with tab2:
        legends = cached_get_underrated_legends(stats_df, movies_df)
        for _, row in legends.iterrows():
            st.markdown(f"<div class='card'><strong>🎬 {row['director']}</strong><br>Avg Rating: {row['avg_rating']:.2f}<br>Top Movies: <em>{row['top_movies']}</em></div>", unsafe_allow_html=True)

    with tab3:
        prolific = cached_get_most_prolific(stats_df, movies_df)
        for _, row in prolific.iterrows():
            st.markdown(f"<div class='card'><strong>🎬 {row['director']}</strong><br>{row['num_movies']} movies<br>Top Movies: <em>{row['top_movies']}</em></div>", unsafe_allow_html=True)

    with tab4:
        viewed = cached_get_most_viewed_directors(stats_df, movies_df)
        for _, row in viewed.iterrows():
            st.markdown(f"<div class='card'><strong>🎬 {row['director']}</strong><br>{row['total_votes']} votes<br>Top Movies: <em>{row['top_movies']}</em></div>", unsafe_allow_html=True)

    with tab5:
        acclaimed = cached_get_popular_and_critically_acclaimed(stats_df, movies_df)
        for _, row in acclaimed.iterrows():
            st.markdown(f"<div class='card'><strong>🎬 {row['director']}</strong><br>Rating: {row['avg_rating']:.2f}, Votes: {row['total_votes']}<br>Top Movies: <em>{row['top_movies']}</em></div>", unsafe_allow_html=True)

    # === 💎 Hidden Gems Section ===
    st.markdown("<div class='section-title'>💎 Hidden Gems</div>", unsafe_allow_html=True)
    hidden = cached_get_hidden_gems(movies_df)
    card_html = ""

    for _, row in hidden.iterrows():
        cast_list = ast.literal_eval(row['cast']) if isinstance(row['cast'], str) else []
        cast_display = ", ".join(cast_list[:5]) if cast_list else "N/A"

        card_html += f"""
        <div class='flip-card'>
            <div class='flip-card-inner'>
                <div class='flip-card-front'>
                    <strong>{row['title']}</strong><br>
                    <em>Director:</em> {row['director']}<br>
                    <em>Rating:</em> {row['average_rating']}<br>
                    <em>Language:</em> {row['language']}<br>
                    <em>Country:</em> {row['countries']}<br>
                    <em>Genres:</em> {row['genres']}<br>
                    <em>Runtime:</em> {row['runtime']} mins<br>
                </div>
                <div class='flip-card-back'>
                    <strong>Description:</strong><br> {row['description']}<br><br>
                    <strong>Cast:</strong><br> {cast_display}
                </div>
            </div>
        </div>
        """
    st.markdown(card_html, unsafe_allow_html=True)

    # === 🎭 Genre-wise Top Movies ===
    st.markdown("<div class='section-title'>🎭 Top Movies by Genre</div>", unsafe_allow_html=True)
    genre_list = [
        "Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary", "Drama", "Family",
        "Fantasy", "History", "Horror", "Music", "Mystery", "Romance",
        "Science", "Fiction", "TV Movie", "Thriller", "War"]
    selected_genre = st.selectbox("Choose a genre to view top-rated movies:", genre_list)

    genre_top_movies = cached_get_top_movies_by_genre(movies_df, selected_genre)
    for _, row in genre_top_movies.iterrows():
        st.markdown(f"<div class='genre-movie'><strong>🎬 {row['title']}</strong></div>", unsafe_allow_html=True)
        st.markdown(f"_Director_: {row['director']} | _Language_: {row['language']} | _Rating_: {row['average_rating']}", unsafe_allow_html=True)
        st.markdown(f"Description: _{row['description']}_", unsafe_allow_html=True)
        st.markdown("---")

    # === 🎭 Actor-Based Leaderboards ===
    st.markdown("<div class='section-title'>🎭 Actor Leaderboards</div>", unsafe_allow_html=True)
    actor_stats_df = cached_load_actor_stats()
    if actor_stats_df.empty:
        st.error("Could not load actor statistics.")
        st.stop()

    actor_tab1, actor_tab2, actor_tab3, actor_tab4 = st.tabs([
        "🏅 Top Rated Actors", "🎭 Versatile Performers", "❤️ Most Liked", "🤝 Frequent Collaborators"
    ])

    with actor_tab1:
        st.markdown("### 🌟 Top Rated Actors")
        sorted_df = st.selectbox("Sort by:", ["Average Rating ↓", "Number of Movies ↓"])
        top_actors = cached_get_top_actors_by_rating(actor_stats_df)
        if sorted_df == "Number of Movies ↓":
            top_actors = top_actors.sort_values(by="num_movies", ascending=False)
        for _, row in top_actors.iterrows():
            st.markdown(f"""
            <div class='card'>
                <strong>🎭 {row['actor']}</strong><br>
                Avg Rating: {row['avg_rating']:.2f}<br>
                Movies: {row['num_movies']}<br>
                Top Roles: <em>{row['top_movies']}</em>
            </div>
            """, unsafe_allow_html=True)

    with actor_tab2:
        st.markdown("### 🎭 Versatile Performers")
        versatile_actors = cached_get_versatile_actors(actor_stats_df)
        for _, row in versatile_actors.iterrows():
            top_3_movies = ", ".join(row['top_movies'].split(",")[:3]) if 'top_movies' in row and row['top_movies'] else "N/A"
            st.markdown(f"""
            <div class='card'>
                <strong>🎭 {row['actor']}</strong><br>
                Unique Genres: {row['unique_genres']}<br>
                Movies: {row['num_movies']}<br>
                Top Genres: <em>{row['top_genres']}</em><br>
                Top 3 Movies: <em>{top_3_movies}</em>
            </div>
            """, unsafe_allow_html=True)

    with actor_tab3:
        st.markdown("### ❤️ Most Liked Actors")
        liked_actors = cached_get_most_liked_actors(actor_stats_df)
        for _, row in liked_actors.iterrows():
            top_3_movies = ", ".join(row['top_movies'].split(",")[:3]) if 'top_movies' in row and row['top_movies'] else "N/A"
            st.markdown(f"""
            <div class='card'>
                <strong>🎭 {row['actor']}</strong><br>
                Likes: {row['likes']}<br>
                Top 3 Movies: <em>{top_3_movies}</em>
            </div>
            """, unsafe_allow_html=True)

    with actor_tab4:
        st.markdown("### 🤝 Frequent Collaborators")

        frequent_collabs = cached_get_most_frequent_collaborators(actor_stats_df)

        for _, row in frequent_collabs.iterrows():
        # Remove memorable collab, add top 3 movies instead
         top_3_movies = ", ".join(row['top_movies'].split(",")[:3]) if 'top_movies' in row and row['top_movies'] else "N/A"

         st.markdown(f"""
         <div class='card'>
            <strong>🎭 {row['actor']}</strong><br>
            Collaborations: {row['shared_movies']}<br>
            Most Frequent Co-Star: <em>{row['frequent_costar']}</em><br>
            <strong>Top 3 Movies:</strong> <em>{top_3_movies}</em>
         </div>
         """, unsafe_allow_html=True)

    # Optional: Visualize leaderboard stats with a graph
    import plotly.express as px

    st.markdown("### 📊 Actor Leaderboard Graph")

    graph_metric = st.selectbox("Choose metric for leaderboard:", ["avg_rating", "num_movies", "likes"])
    top_n = st.slider("Top N actors to display:", min_value=5, max_value=20, value=10)

    chart_df = actor_stats_df.nlargest(top_n, graph_metric)
    fig = px.bar(
     chart_df,
     x="actor",
     y=graph_metric,
     color=graph_metric,
     text_auto='.2s',
     color_continuous_scale="sunsetdark",
     title=f"Top {top_n} Actors by {graph_metric.replace('_', ' ').title()}",
     labels={graph_metric: graph_metric.replace("_", " ").title(), "actor": "Actor"}
    )
    fig.update_layout(xaxis_tickangle=-45, title_font_size=20, plot_bgcolor="#111827", paper_bgcolor="#111827", font_color="white")
    st.plotly_chart(fig, use_container_width=True)
        



