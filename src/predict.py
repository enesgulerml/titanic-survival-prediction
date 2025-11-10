# src/predict.py

import pandas as pd
import joblib
import sys
from pathlib import Path

# We pull the necessary paths from Config
from src.config import (
    MODEL_OUTPUT_PATH,
    TEST_DATA_PATH,
    SUBMISSION_PATH
)


def run_prediction():
    """
    It loads the trained model and performs a batch prediction on the 'test.csv' data.
    It saves the results as 'submission.csv'.
    """
    print("===== Initiating the Forecast Process =====")

    # 1. Install Trained Pipeline
    # We load the .joblib file that we saved in 'train.py'.
    try:
        model = joblib.load(MODEL_OUTPUT_PATH)
        print(f"The model was loaded from {MODEL_OUTPUT_PATH}.")
    except FileNotFoundError:
        print(f"ERROR: Model file not found. Please run 'python -m src.train' command first.")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading model: {e}")
        sys.exit(1)

    # 2.
    # This is the 'test.csv' file we downloaded from Kaggle
    try:
        X_new = pd.read_csv(TEST_DATA_PATH)
        print(f"New data was loaded from {TEST_DATA_PATH}.")
    except FileNotFoundError:
        print(f"ERROR: {TEST_DATA_PATH} file not found.")
        sys.exit(1)

    # === MAGICAL MOMENT ===

    print("Predictions are being made...")
    predictions = model.predict(X_new)
    print("Predictions are complete.")

    # 4. Create Submission File
    # The format Kaggle requires from us: PassengerId and Survived columns
    # PassengerId column already exists in file 'test.csv'.
    submission = pd.DataFrame({
        'PassengerId': X_new['PassengerId'],
        'Survived': predictions
    })

    # 5.
    try:
        SUBMISSION_PATH.parent.mkdir(parents=True, exist_ok=True)

        submission.to_csv(SUBMISSION_PATH, index=False)
        print(f"Prediction results successfully saved to: {SUBMISSION_PATH}")
        print("===== Estimation Process Completed =====")
    except Exception as e:
        print(f"Error occurred while saving submission file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run_prediction()