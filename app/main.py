# app/main.py

import joblib
import pandas as pd
from fastapi import FastAPI
from app.schema import Passenger, PredictionResponse
from typing import List

# === Reward for the Work We Did in v1.0 and v2.0 ===
from src.config import MODEL_OUTPUT_PATH, TEST_DATA_PATH

# --- Installing the Application and Model ---
app = FastAPI(
    title="Titanic Survival Prediction API",
    description="v3.0 - A 'Google-level' API service for the Titanic pipeline.",
    version="3.0.0"
)


@app.on_event("startup")
def load_model():
    print("API is starting and loading v2.1 model...")
    try:
        app.state.model = joblib.load(MODEL_OUTPUT_PATH)
        print(f"Model successfully loaded from {MODEL_OUTPUT_PATH}.")
    except FileNotFoundError:
        print(f"ERROR: Model not found at {MODEL_OUTPUT_PATH}.")
        print("Please make sure to run 'python -m src.train' before running the API.")
        app.state.model = None

# --- API Endpoints ---

@app.get("/", tags=["Health Check"])
def read_root():
    """The root endpoint checks whether the API is running."""
    return {"status": "ok", "message": "Titanic Prediction API is running!"}

@app.post("/predict",
          response_model=PredictionResponse,
          tags=["Prediction"])
def predict_survival(passenger: Passenger):
    """
    It estimates survival by taking data from a single passenger.

    Thanks to Pydantic (Passenger schema), incoming data ('Age', 'Sex', etc.) is guaranteed to be in the correct format.
    """
    if app.state.model is None:
        return {"error": "Model is not loaded."}

    # 1. Convert Pydantic model to a DataFrame
    input_data = pd.DataFrame([passenger.model_dump()])

    # 2. Predict
    prediction = app.state.model.predict(input_data)[0]

    # 3. Return the result in a format that matches the Pydantic response model
    return {"Survived": prediction}