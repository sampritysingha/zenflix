import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the cleaned movies dataset
def load_movie_data(path='data/processed/movies_cleaned_final.csv'):
    return pd.read_csv(path)

# TF-IDF based genre similarity
def get_genre_similarity_matrix(df):
    tfidf = TfidfVectorizer(stop_words='english')
    genre_matrix = tfidf.fit_transform(df['genres'].fillna(''))
    return genre_matrix, tfidf

# Zodiac assignment logic
def assign_zodiac_roles(df, user_movies):
    df['sentiment_score'] = df['sentiment_polarity'].fillna(0)  # Use sentiment_polarity from the dataset
    
    genre_matrix, _ = get_genre_similarity_matrix(df)

    zodiac_chart = {}
    roles = ['Sun', 'Moon', 'Rising']

    for i, user_movie in enumerate(user_movies):
        if user_movie not in df['title'].values:
            zodiac_chart[roles[i]] = f"'{user_movie}' not found in dataset"
            continue

        user_idx = df[df['title'] == user_movie].index[0]
        user_vector = genre_matrix[user_idx]
        similarities = cosine_similarity(user_vector, genre_matrix).flatten()

        # Exclude the movie itself and take next top match
        similarities[user_idx] = -1
        best_match_idx = np.argmax(similarities)

        match = df.iloc[best_match_idx]

        # Explanation for the genre similarity and sentiment polarity match
        genre_similarity_score = round(similarities[best_match_idx], 3)
        sentiment_score = match['sentiment_score']
        sentiment_reason = "positive sentiment" if sentiment_score > 0 else "negative sentiment" if sentiment_score < 0 else "neutral sentiment"

        genre_explanation = f"The genre similarity score of {genre_similarity_score} indicates that the genres of {user_movie} and {match['title']} are highly aligned."
        sentiment_explanation = f"The sentiment polarity score of {sentiment_score} indicates a {sentiment_reason}, reflecting your emotional connection to the movie."

        # Combine everything for the explanation
        zodiac_chart[roles[i]] = {
            'Your Pick': user_movie,
            'Zodiac Match': match['title'],
            'Genre Similarity': genre_similarity_score,
            'Sentiment Polarity Score': sentiment_score,
            'Reason for Genre Similarity': genre_explanation,
            'Reason for Sentiment Match': sentiment_explanation,
            'Zodiac Role': f"Your {roles[i]} movie is {match['title']} because it aligns with your {roles[i].lower()} traits.",
            'Director': match.get('director', 'N/A'),
            'Genre': match.get('genres', 'N/A'),
            'Description': match.get('description', 'N/A')
        }

    return zodiac_chart
