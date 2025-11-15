# test/test_train_integration.py

import pytest
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from pathlib import Path

# Import the core components to be tested
from src.data_processing import load_data, split_features_target
from src.pipeline import create_pipeline
from src.config import (
    TEST_SIZE,
    RANDOM_STATE,
    TARGET_VARIABLE,
    MODEL_OUTPUT_PATH
)


# Mark this test as 'slow'
@pytest.mark.slow
def test_full_training_integration_pipeline():
    """
    Test v5.2 (Integration Test):
    Validates the entire v1.0 (Training) pipeline.

    This test ensures that:
    1. 'load_data()' and 'split_features_target()' run successfully.
    2. 'create_pipeline()' (RandomForest) runs successfully.
    3. The components integrate correctly during 'pipeline.fit()'.
    4. The resulting accuracy score meets the minimum performance threshold.

    Note: This test requires the raw data file ('train.csv')
    to be present in the 'data/raw/' directory.
    """

    # --- 1. Arrange ---
    # Attempt to load the raw data.
    try:
        data = load_data()
        X, y = split_features_target(data)
    except FileNotFoundError:
        pytest.fail(
            "Integration Test Failed: 'data/raw/train.csv' not found. "
            "This test requires the raw data to run."
        )
    except Exception as e:
        pytest.fail(f"Integration Test Failed: Data loading/splitting "
                    f"raised an exception: {e}")

    # --- 2. Act ---
    # Replicate the core logic from 'src/train.py'
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE
    )

    pipeline = create_pipeline()
    pipeline.fit(X_train, y_train)
    preds = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, preds)

    # --- 3. Assert ---
    # Verify the integrity and performance of the integrated pipeline

    print(f"\nIntegration Test Accuracy Score: {accuracy}")

    # Assertion 1: Check for complete model failure (worse than baseline)
    # A simple baseline (e.g., "all died") would be ~61%
    assert accuracy > 0.65, (f"Accuracy ({accuracy}) is below the 0.65 baseline. "
                             f"The model is performing poorly.")

    # Assertion 2: Check for performance regression
    # This is a specific threshold based on our v1.0 (RandomForest) model.
    expected_accuracy_threshold = 0.80
    assert accuracy >= expected_accuracy_threshold, (
        f"Accuracy ({accuracy:.4f}) is below the expected threshold of "
        f"{expected_accuracy_threshold}. A model regression may have occurred."
    )