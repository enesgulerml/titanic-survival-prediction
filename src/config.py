# src/config.py

# === 1. File Paths ===
TRAIN_DATA_PATH = "data/raw/train.csv"
TEST_DATA_PATH = "data/raw/test.csv"

MODEL_OUTPUT_PATH = "models/titanic_model.joblib"


# === 2. Target Variable ===
TARGET_VARIABLE = "Survived"


# === 3. Feature Lists ===
# These lists tell the scikit-learn pipeline what to do with each column.

# Numerical Properties (Pipeline will Impute/Scale these)
NUMERICAL_FEATURES = ["Age", "Fare", "SibSp", "Parch"]

# Categorical Features (Pipeline will Impute/OneHotEncode them)
CATEGORICAL_FEATURES = ["Sex", "Embarked", "Pclass"]

# Features to be discarded (columns that do not need to be included in the model and create noise)
DROP_FEATURES = ["PassengerId", "Name", "Ticket", "Cabin"]


# === 4. Model and Data Separation Settings ===
# How much of the data will be allocated for testing
TEST_SIZE = 0.2

# To ensure that the results are the same in each run (reproducibility)
RANDOM_STATE = 42