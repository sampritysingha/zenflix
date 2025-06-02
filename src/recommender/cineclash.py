# backend.py
import pandas as pd
import random

# Load the datasets
movies_df = pd.read_csv(r"C:\Users\sampr\OneDrive\Documents\zenflix\data\processed\movies_cleaned_final.csv")
directors_df = pd.read_csv(r"C:\Users\sampr\OneDrive\Documents\zenflix\data\processed\director_stats.csv")

# Filter function based on mood
mood_keywords = {
    "Happy / Cheerful": [
        "Comedy", "Musical", "Romance", "Adventure", "Family", "Animation"
    ],
    "Sad / Heartbroken": [
        "Drama", "Romance", "Documentary", "Animation", "Family"
    ],
    "Angry / Frustrated": [
        "Action", "Thriller", "Crime", "Drama"
    ],
    "Anxious / Overwhelmed": [
        "Comedy", "Family", "Animation", "Romance", "Documentary"
    ],
    "Bored / Restless": [
        "Mystery", "Science Fiction", "Thriller", "Adventure", "Fantasy", "Crime"
    ],
    "Romantic / Dreamy": [
        "Romance", "Drama", "Fantasy", "Music", "Animation"
    ],
    "Curious / Thoughtful": [
        "Mystery", "Science Fiction", "Documentary", "Drama", "History", "Biopic"
    ],
    "Lonely / Nostalgic": [
        "Coming-of-age", "Family", "Drama", "Animation", "History"
    ],
    "Playful / Mischievous": [
        "Comedy", "Teen", "Satire", "Parody", "Dark Comedy"
    ],
    "Inspired / Motivated": [
        "Documentary", "Drama", "Biography", "War", "Sports", "History"
    ]
}



def suggest_movies(mood):
    keywords = mood_keywords.get(mood, [])
    filtered = movies_df[movies_df['clean_genres'].str.contains('|'.join(keywords), case=False, na=False)]
    return filtered.sample(n=5) if len(filtered) >= 5 else filtered.sample(n=5, replace=True)

def get_director_score(director_name):
    row = directors_df[directors_df['director'] == director_name]
    return row['popularity_score'].values[0] if not row.empty else 0

def get_movie_stats(movie_row):
    return {
        "title": movie_row["title"],
        "list_appearances": movie_row["list_appearances"],
        "watch_count": movie_row["watch_count"],
        "avg_rating_norm": movie_row["avg_rating_norm"],
        "likes": movie_row["likes"],
        "fans": movie_row["fans"],
        "director_score": get_director_score(movie_row["director"])
    }

def compare_movies(movie1_title, movie2_title):
    m1 = movies_df[movies_df["title"] == movie1_title].iloc[0]
    m2 = movies_df[movies_df["title"] == movie2_title].iloc[0]

    stats1 = get_movie_stats(m1)
    stats2 = get_movie_stats(m2)

    keys = ["list_appearances", "watch_count", "avg_rating_norm", "likes", "fans", "director_score"]
    score1, score2 = 0, 0

    for key in keys:
        if stats1[key] > stats2[key]:
            score1 += 1
        elif stats1[key] < stats2[key]:
            score2 += 1

    return stats1, stats2, score1, score2
