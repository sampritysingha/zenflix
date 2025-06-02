import pandas as pd
from collections import Counter, defaultdict
from ast import literal_eval

def load_movies_data(path):
    """
    Loads the cleaned movies dataset and parses cast.
    """
    try:
        df = pd.read_csv(path)
        df['cast'] = df['cast'].apply(lambda x: literal_eval(x) if isinstance(x, str) else [])
        df['genres'] = df['genres'].apply(lambda x: literal_eval(x) if isinstance(x, str) else [])
        return df
    except FileNotFoundError:
        print(f"File not found at {path}")
        return pd.DataFrame()

# === 1. load_actor_stats ===
def load_actor_stats(path=r"C:\Users\sampr\OneDrive\Documents\zenflix\data\processed\movies_cleaned_final.csv"):
    """
    Loads actor statistics from the movie dataset.
    Returns a DataFrame with actor-level aggregates.
    """
    df = load_movies_data(path)
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

# === 2. get_top_actors_by_rating ===
def get_top_actors_by_rating(actor_df, top_n=5):
    """
    Returns top actors based on average rating.
    """
    return actor_df.sort_values(by='avg_rating', ascending=False).head(top_n)

# === 3. get_versatile_actors ===
def get_versatile_actors(actor_df, top_n=5):
    """
    Returns actors with highest number of unique genres.
    """
    return actor_df.sort_values(by='unique_genres', ascending=False).head(top_n)

# === 4. get_most_liked_actors ===
def get_most_liked_actors(actor_df, top_n=5):
    """
    Returns actors based on total likes and 5-star count.
    """
    return actor_df.sort_values(by=["likes", "five_star_count"], ascending=False).head(top_n)

# === 5. get_most_frequent_collaborators ===
def get_most_frequent_collaborators(actor_df, top_n=5):
    """
    Returns actors based on most frequent co-stars.
    """
    return actor_df[actor_df['frequent_costar'] != "N/A"].sort_values(by="shared_movies", ascending=False).head(top_n)

# === OPTIONAL: CLI Debugging ===
if __name__ == "__main__":
    df_stats = load_actor_stats(r"C:\Users\sampr\OneDrive\Documents\zenflix\data\processed\movies_cleaned_final.csv")
    print(df_stats.head(10))
    print("\nTop Rated:\n", get_top_actors_by_rating(df_stats))
    print("\nVersatile:\n", get_versatile_actors(df_stats))
    print("\nLiked:\n", get_most_liked_actors(df_stats))
    print("\nCollaborators:\n", get_most_frequent_collaborators(df_stats))
