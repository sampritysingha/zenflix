import pandas as pd
from collections import Counter, defaultdict
from ast import literal_eval
from src.utils.data_loader import load_movie_data


def safe_literal_eval(val):
    """
    Safely evaluate a string representation of a Python literal.
    Returns an empty list if evaluation fails or input is not a string.
    """
    try:
        return literal_eval(val) if isinstance(val, str) else []
    except Exception:
        return []


def load_movies_data():
    """
    Load movie data with 'cast' and 'genres' columns converted from strings to lists.
    Uses centralized loader from utils for consistent path handling.
    
    Returns:
        pd.DataFrame: Movie dataset with parsed cast and genres columns.
    """
    df = load_movie_data()
    if df.empty:
        return pd.DataFrame()

    df['cast'] = df['cast'].apply(safe_literal_eval)
    df['genres'] = df['genres'].apply(safe_literal_eval)
    return df


def load_actor_stats():
    """
    Aggregate actor statistics from movie data.

    Returns:
        pd.DataFrame: Actor stats with number of movies, average rating, likes,
                      frequent collaborators, top genres and movies, etc.
    """
    df = load_movies_data()
    if df.empty:
        return pd.DataFrame()

    actor_data = defaultdict(lambda: {
        "num_movies": 0,
        "total_rating": 0,
        "likes": 0,
        "five_star_count": 0,
        "genres": [],
        "costars": [],
        "top_movies": []
    })

    for _, row in df.iterrows():
        for actor in row['cast']:
            actor_data[actor]["num_movies"] += 1
            actor_data[actor]["total_rating"] += row.get("average_rating", 0)
            actor_data[actor]["likes"] += row.get("likes", 0)
            actor_data[actor]["five_star_count"] += int(row.get("five_star_count", 0))
            actor_data[actor]["genres"].extend(row.get("genres", []))
            actor_data[actor]["costars"].extend([a for a in row['cast'] if a != actor])
            actor_data[actor]["top_movies"].append((row['title'], row.get("average_rating", 0)))

    records = []
    for actor, data in actor_data.items():
        avg_rating = data["total_rating"] / data["num_movies"] if data["num_movies"] > 0 else 0
        top_movies = sorted(data["top_movies"], key=lambda x: -x[1])[:3]
        top_movie_titles = ", ".join([t for t, _ in top_movies])
        genre_counts = Counter(data["genres"]).most_common(3)
        top_genres = ", ".join([g for g, _ in genre_counts])
        most_common_costar = Counter(data["costars"]).most_common(1)
        costar_name = most_common_costar[0][0] if most_common_costar else "N/A"
        shared_movies = most_common_costar[0][1] if most_common_costar else 0

        records.append({
            "actor": actor,
            "num_movies": data["num_movies"],
            "avg_rating": round(avg_rating, 2),
            "likes": data["likes"],
            "five_star_count": data["five_star_count"],
            "unique_genres": len(set(data["genres"])),
            "top_genres": top_genres,
            "top_movies": top_movie_titles,
            "frequent_costar": costar_name,
            "shared_movies": shared_movies,
            "top_collabs": f"{costar_name} ({shared_movies} films)"
        })

    return pd.DataFrame(records)


def get_top_actors_by_rating(actor_df, top_n=5):
    """
    Get top actors sorted by average rating.
    """
    return actor_df.sort_values(by='avg_rating', ascending=False).head(top_n)


def get_versatile_actors(actor_df, top_n=5):
    """
    Get actors with most diverse genre involvement.
    """
    return actor_df.sort_values(by='unique_genres', ascending=False).head(top_n)


def get_most_liked_actors(actor_df, top_n=5):
    """
    Get actors with highest likes and five-star counts.
    """
    return actor_df.sort_values(by=["likes", "five_star_count"], ascending=False).head(top_n)


def get_most_frequent_collaborators(actor_df, top_n=5):
    """
    Get actors with most frequent collaborators.
    """
    return actor_df[actor_df['frequent_costar'] != "N/A"].sort_values(by="shared_movies", ascending=False).head(top_n)


if __name__ == "__main__":
    df_stats = load_actor_stats()
    print(df_stats.head(10))
    print("\nTop Rated:\n", get_top_actors_by_rating(df_stats))
    print("\nVersatile:\n", get_versatile_actors(df_stats))
    print("\nLiked:\n", get_most_liked_actors(df_stats))
    print("\nCollaborators:\n", get_most_frequent_collaborators(df_stats))
