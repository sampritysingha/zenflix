import pandas as pd
import os

DATA_PATH = "data/processed"

def load_director_stats():
    """
    Load the director_stats.csv file containing director-based statistics.
    """
    file_path = os.path.join(DATA_PATH, r"C:\Users\sampr\OneDrive\Documents\zenflix\data\processed\director_stats.csv")
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"Missing file: {file_path}")

def load_movie_data():
    """
    Load the movies_cleaned.csv file containing movie-level information.
    """
    file_path = os.path.join(DATA_PATH, r"C:\Users\sampr\OneDrive\Documents\zenflix\data\processed\movies_cleaned_final.csv")
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"Missing file: {file_path}")
