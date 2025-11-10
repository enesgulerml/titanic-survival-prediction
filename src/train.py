# src/train.py

import pandas as pd
from sklearn.model_selection import train_test_split
from joblib import dump  # To save the model to disk
import sys  # To exit in case of error

# Let's import functions and settings from our other .py files
from src.config import (
    MODEL_OUTPUT_PATH,
    TEST_SIZE,
    RANDOM_STATE
)
from src.data_processing import load_data, split_features_target
from src.pipeline import create_pipeline

def run_training():
    """
    Manages the main educational process.
    """
    print("===== The Training Process is Starting =====")

    # 1. Load Data
    data = load_data()
    if data is None:
        print("ERROR: Failed to load data. Stopping training.")
        sys.exit(1) # Terminate the program with an error code

    # 2. Separate into Features (X) and Target (y)
    X, y = split_features_target(data)
    if X is None or y is None:
        print("ERROR: Data could not be separated into X and y. Stopping training.")
        sys.exit(1)

    # 3. Split into Training and Test Sets (Preventing Data Leakage)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE
    )
    print(f"Data was split into training and test sets. (Test size: {TEST_SIZE})")
    print(f"Training set size: {X_train.shape[0]}, Test set size: {X_test.shape[0]}")

    # 4. Create the Pipeline
    pipeline = create_pipeline()

    # 5. TRAIN Pipeline (WITH TRAINING DATA ONLY)
    print("Pipeline training (fit) begins...")
    pipeline.fit(X_train, y_train)
    print("Pipeline training has been completed.")

    # 6. Evaluate Pipeline (WITH TEST DATA ONLY)
    accuracy = pipeline.score(X_test, y_test)
    print(f"The accuracy score of the model on the test data: {accuracy:.4f}")

    # 7. Save Trained Pipeline
    print(f"The trained model (pipeline) is saved to: {MODEL_OUTPUT_PATH}")
    dump(pipeline, MODEL_OUTPUT_PATH)
    print("The model has been successfully saved.")
    print("===== The Training Process Has Been Completed =====")


if __name__ == "__main__":
    run_training()