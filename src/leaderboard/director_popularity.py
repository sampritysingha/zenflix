import pandas as pd
import os

def load_movies_data():
    """Loads the cleaned movie data used for top movies by director and genre-based queries."""
    data_path = os.path.join("data", "processed", r"c:\Users\sampr\OneDrive\Documents\zenflix\data\processed\movies_cleaned_final.csv")
    if not os.path.exists(data_path):
        print(f"File not found: {data_path}")
        return pd.DataFrame()
    return pd.read_csv(data_path)


def load_director_stats(path=r'C:\Users\sampr\OneDrive\Documents\zenflix\data\processed\director_stats.csv'):
    """Loads director statistics from the processed data folder."""
    try:
        df = pd.read_csv(path)
        return df
    except FileNotFoundError:
        print(f"File not found at {path}")
        return pd.DataFrame()

def get_top_movies_by_director(movies_df, director_name, top_n=3):
    """Returns a comma-separated string of top N movie titles for a given director, sorted by rating."""
    director_movies = movies_df[movies_df['director'].str.lower() == director_name.lower()]
    if director_movies.empty:
        return "N/A"
    top_movies = director_movies.sort_values(by='average_rating', ascending=False).head(top_n)
    return ", ".join(top_movies['title'].fillna("Unknown").tolist())

def get_top_directors(director_df, movies_df, top_n=5, min_movies=3):
    """
    Returns a leaderboard of top directors with their top 3 movies.
    """
    df_filtered = director_df[director_df['num_movies'] >= min_movies]
    leaderboard = df_filtered.sort_values(by='avg_rating', ascending=False).head(top_n).copy()
    leaderboard['top_movies'] = leaderboard['director'].apply(
        lambda name: get_top_movies_by_director(movies_df, name, top_n=3)
    )
    return leaderboard.reset_index(drop=True)

def get_underrated_legends(stats_df, movies_df, max_movies=2, min_rating=4.0, top_n=5):
    legends = stats_df[(stats_df['num_movies'] <= max_movies) & (stats_df['avg_rating'] >= min_rating)]
    legends_sorted = legends.sort_values(by='avg_rating', ascending=False).head(top_n).copy()
    legends_sorted['top_movies'] = legends_sorted['director'].apply(lambda x: get_top_movies_by_director(movies_df, x))
    return legends_sorted.reset_index(drop=True)

def get_most_prolific(stats_df, movies_df, top_n=5):
    prolific = stats_df.sort_values(by='num_movies', ascending=False).head(top_n).copy()
    prolific['top_movies'] = prolific['director'].apply(lambda x: get_top_movies_by_director(movies_df, x))
    return prolific.reset_index(drop=True)

def get_most_viewed_directors(stats_df, movies_df, top_n=5):
    viewed = stats_df.sort_values(by='total_votes', ascending=False).head(top_n).copy()
    viewed['top_movies'] = viewed['director'].apply(lambda x: get_top_movies_by_director(movies_df, x))
    return viewed.reset_index(drop=True)

def get_popular_and_critically_acclaimed(stats_df, movies_df, min_votes=50000, min_rating=4.0, top_n=5):
    filtered = stats_df[(stats_df['total_votes'] >= min_votes) & (stats_df['avg_rating'] >= min_rating)]
    sorted_df = filtered.sort_values(by='avg_rating', ascending=False).head(top_n).copy()
    sorted_df['top_movies'] = sorted_df['director'].apply(lambda x: get_top_movies_by_director(movies_df, x))
    return sorted_df.reset_index(drop=True)

def get_hidden_gems(movies_df, max_watch_count=5000, min_rating=4.0, top_n=10):
    gems = movies_df[(movies_df['watch_count'] <= max_watch_count) & (movies_df['average_rating'] >= min_rating)]
    gems_sorted = gems.sort_values(by=['average_rating', 'watch_count'], ascending=[False, True])
    return gems_sorted[['title', 'director', 'language', 'cast', 'description', 'genres','countries','runtime', 'average_rating']].head(top_n).reset_index(drop=True)


def get_top_movies_by_genre(movies_df, genre, top_n=5):
    genre_df = movies_df[movies_df['genres'].str.contains(genre, case=False, na=False)]
    top_movies = genre_df.sort_values(by='average_rating', ascending=False).head(top_n)
    return top_movies[['title', 'genres', 'average_rating', 'description','director', 'language']].reset_index(drop=True)
