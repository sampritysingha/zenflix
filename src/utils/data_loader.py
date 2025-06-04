import os
import pandas as pd

def load_movie_data():
    """
    Load processed movie data from CSV.
    
    Returns:
        pd.DataFrame: DataFrame with movie data or empty DataFrame if file not found.
    """
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    data_path = os.path.join(root_dir, "data", "processed", "movies_cleaned_final.csv")
    if not os.path.exists(data_path):
        print(f"File not found: {data_path}")
        return pd.DataFrame()
    return pd.read_csv(data_path)

def load_director_stats():
    """
    Load processed director statistics data from CSV.
    
    Returns:
        pd.DataFrame: DataFrame with director stats or empty DataFrame if file not found.
    """
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    path = os.path.join(root_dir, "data", "processed", "director_stats.csv")
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return pd.DataFrame()
    return pd.read_csv(path)
