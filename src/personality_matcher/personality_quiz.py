import pandas as pd

# Load and preprocess movie data
def load_movie_data(csv_path=r'C:\Users\sampr\OneDrive\Documents\zenflix\data\processed\movies_cleaned_final.csv'):
    df = pd.read_csv(csv_path)

    # Ensure sentiment_polarity column exists, else create neutral sentiment (0)
    if 'sentiment_polarity' not in df.columns:
        df['sentiment_polarity'] = 0.0

    return df

# Normalize sentiment polarity from [-1,1] to [0,1]
def normalize_sentiment(score):
    return (score + 1) / 2

# Match movie by sentiment score from quiz answers (user_sentiment normalized to [0,1])
def match_movie_by_sentiment(user_sentiment, df):
    # Normalize movie sentiment polarity to [0,1] for fair comparison
    df['sentiment_norm'] = df['sentiment_polarity'].apply(normalize_sentiment)

    df['sentiment_diff'] = (df['sentiment_norm'] - user_sentiment).abs()

    best_match = df.sort_values(by='sentiment_diff').iloc[0]

    # Ensure Cast is a list for frontend display
    cast_list = []
    if isinstance(best_match['cast'], str):
        cast_list = [c.strip() for c in best_match['cast'].split(',')]
    elif isinstance(best_match['cast'], list):
        cast_list = best_match['cast']
    else:
        cast_list = []

    sentiment_match_score = round(1 - best_match['sentiment_diff'], 2)

    return {
        "🎬 You are...": best_match['title'],
        "📖 Description": best_match['description'],
        "Genres": best_match['genres'],
        "Director": best_match['director'],
        "Language": best_match['language'],
        "Cast": cast_list,
        "Rating": best_match['average_rating'],
        "🌡 Sentiment Match Score": sentiment_match_score,
        "🧠 Why?": f"This movie reflects your emotional tone and personality with a sentiment match score of {sentiment_match_score}."
    }

# Convert answers to sentiment score between 0 and 1
def run_personality_quiz(answers):
    # Example: answers are 1 to 4 per question; convert to 0-1 scale averaging all answers
    max_answer_val = 4
    user_sentiment = sum(answers) / (len(answers) * max_answer_val)  # normalized [0,1]

    df = load_movie_data()

    result = match_movie_by_sentiment(user_sentiment, df)

    return result
