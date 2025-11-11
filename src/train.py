# src/train.py

import pandas as pd
from sklearn.model_selection import train_test_split
from joblib import dump
import sys
import mlflow
import mlflow.sklearn
import datetime

# Let's import functions and settings from our other .py files
from src.config import (
    MODEL_OUTPUT_PATH,
    TEST_SIZE,
    RANDOM_STATE,
    MLFLOW_EXPERIMENT_NAME,
    NUMERICAL_FEATURES,
    CATEGORICAL_FEATURES
)
from src.data_processing import load_data, split_features_target
from src.pipeline import create_pipeline


def run_training():
    """
    Manages the main training process.

    Records parameters, metrics, and the model with MLFlow.
    """
    print("===== Starting the Training Process (v2.0 - with MLFlow) =====")

    # === Start the MLFlow Experiment ===
    mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)

    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    run_name = f"run_{current_time}"

    with mlflow.start_run(run_name=run_name):

        mlflow.set_tag("description", "Standard RandomForest training run.")
        mlflow.set_tag("run_name", run_name)

        # 1. Load Data
        data = load_data()
        if data is None:
            print("ERROR: Failed to load data. Stopping training.")
            sys.exit(1)

        # 2. Separate into Features (X) and Target (y)
        X, y = split_features_target(data)
        if X is None or y is None:
            print("ERROR: Data could not be separated into X and y. Stopping training.")
            sys.exit(1)

        # 3. Split into Training and Test Sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=TEST_SIZE,
            random_state=RANDOM_STATE
        )
        print(f"Data was split into training and test sets. (Test size: {TEST_SIZE})")

        # --- MLFlow Registration Step 1: Parameters ---
        print("Saving parameters to MLFlow...")
        mlflow.log_param("test_size", TEST_SIZE)
        mlflow.log_param("random_state", RANDOM_STATE)
        mlflow.log_param("numerical_features_count", len(NUMERICAL_FEATURES))
        mlflow.log_param("categorical_features_count", len(CATEGORICAL_FEATURES))

        # 4. Create the Pipeline
        pipeline = create_pipeline()

        # 5. TRAIN Pipeline
        print("Pipeline training (fit) begins...")
        pipeline.fit(X_train, y_train)
        print("Pipeline training has been completed.")

        # 6. Evaluate Pipeline
        accuracy = pipeline.score(X_test, y_test)
        print(f"The accuracy score of the model on the test data: {accuracy:.4f}")

        # --- MLFlow Recording Step 2: Metrics ---
        print("Saving metrics to MLFlow...")
        mlflow.log_metric("accuracy", accuracy)

        # 7. Save Trained Pipeline (Locally)
        print(f"The trained model (pipeline) is saved to: {MODEL_OUTPUT_PATH}")

        # Make sure the 'models/' folder exists before saving
        MODEL_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

        dump(pipeline, MODEL_OUTPUT_PATH)
        print("The model has been successfully saved.")

        # --- MLFlow Registration Step 3: Model (Artifact) ---
        print("Saving model (artifact) to MLFlow...")
        mlflow.sklearn.log_model(
            sk_model=pipeline,
            artifact_path="model",
            input_example=X_train.head()
        )

        print("===== Training Process Completed (MLFlow) =====")


if __name__ == "__main__":
    run_training()