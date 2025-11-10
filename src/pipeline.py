# src/pipeline.py

from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier

# We make our imports from our 'config.py' file
from src.config import (
    NUMERICAL_FEATURES,
    CATEGORICAL_FEATURES,
    DROP_FEATURES,
    RANDOM_STATE
)


def create_pipeline() -> Pipeline:
    """
    It creates the scikit-learn pipeline, which includes all data processing and modeling steps.

    :return: Training-ready scikit-learn Pipeline object
    """

    # === 1. Sub-Pipeline for Numerical Properties ===
    # Steps to apply to numeric columns
    # Step 1: Fill missing values (NaN) with the median of the column
    # Step 2: Standardize the data (StandardScaler)
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    # === 2. Sub-Pipeline for Categorical Features ===
    # Steps to apply to categorical columns
    # Step 1: Fill in missing values (NaN) with the most frequent value (mode)
    # Step 2: Convert columns to vectors with One-Hot Encoding
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    # === 3. ColumnTransformer ===
    # This tool manages which pipeline is applied to which column.
    # We use the lists we read from 'config.py' here.
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, NUMERICAL_FEATURES),
            ('cat', categorical_transformer, CATEGORICAL_FEATURES),
            ('drop', 'drop', DROP_FEATURES)
        ],
        remainder='drop'
    )

    # === 4. Main Pipeline (Big Picture) ===
    # Combines all steps
    model_pipeline = Pipeline(steps=[
        # Step 1: Data preprocessing (Numeric and Categorical transformations)
        ('preprocessor', preprocessor),

        # Step 2: Model (Takes the cleaned data and starts training)
        ('classifier', RandomForestClassifier(random_state=RANDOM_STATE))
    ])

    print("scikit-learn pipeline created successfully.")
    return model_pipeline