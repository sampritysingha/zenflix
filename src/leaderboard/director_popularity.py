import pandas as pd
from src.utils.data_loader import load_movie_data, load_director_stats


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


# Example usage inside this file for testing (optional)
if __name__ == "__main__":
    movies_df = load_movie_data()
    director_df = load_director_stats()
    print(get_top_directors(director_df, movies_df))
