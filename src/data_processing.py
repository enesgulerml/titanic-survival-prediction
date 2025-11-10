# src/data_processing.py

import pandas as pd

from src.config import TRAIN_DATA_PATH, TARGET_VARIABLE


def load_data(path: str = TRAIN_DATA_PATH) -> pd.DataFrame:
    """
    Loads raw data from the specified path (by default, TRAIN_DATA_PATH in the config).

    :param path: Path of CSV file to upload
    :return: pandas DataFrame
    """
    try:
        data = pd.read_csv(path)
        print(f"Data successfully loaded from {path}.")
        return data
    except FileNotFoundError:
        print(f"ERROR: Data file not found at {path}.")
        print("Please place the files you downloaded from Kaggle in the 'data/raw/' folder.")
        print("Make sure you copy the train.csv and test.csv files.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while loading data: {e}")
        return None


def split_features_target(data: pd.DataFrame, target: str = TARGET_VARIABLE) -> (pd.DataFrame, pd.Series):
    """
    It separates the dataset into features (X) and target (y).

    :param data: DataFrame containing properties and target
    :param target: target column name from config
    :return: (X, y) tuple
    """
    if target not in data.columns:
        print(f"ERROR: Target column '{target}' not found in DataFrame.")
        return None, None

    X = data.drop(target, axis=1)
    y = data[target]
    print("The data was separated into features (X) and target (y).")
    return X, y