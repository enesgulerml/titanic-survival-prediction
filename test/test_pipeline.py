# test/test_pipeline.py

import pytest
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

# Import the function to be tested from the source code
# This works because the 'src' package is installed via 'pip install -e .'
from src.pipeline import create_pipeline


def test_create_pipeline_returns_pipeline_object():
    """
    Test 1 (Unit Test):
    Validates that the create_pipeline function successfully returns
    a scikit-learn Pipeline object.
    """
    # Act: Call the function
    pipeline = create_pipeline()

    # Assert: Check if the returned object is an instance of Pipeline
    assert isinstance(pipeline, Pipeline)


def test_create_pipeline_has_correct_steps():
    """
    Test 2 (Structural Test):
    Validates that the pipeline contains the two mandatory named steps:
    'preprocessor' and 'classifier'.
    """
    # Act
    pipeline = create_pipeline()

    # Assert: Check for the existence of named steps
    assert "preprocessor" in pipeline.named_steps
    assert "classifier" in pipeline.named_steps


def test_create_pipeline_uses_randomforest_by_default():
    """
    Test 3 (Model Validation Test):
    Validates that the 'classifier' step in the pipeline is
    an instance of RandomForestClassifier, as expected for this project.
    """
    # Act
    pipeline = create_pipeline()

    # Assert: Isolate the classifier step and check its type
    classifier_step = pipeline.named_steps['classifier']
    assert isinstance(classifier_step, RandomForestClassifier)