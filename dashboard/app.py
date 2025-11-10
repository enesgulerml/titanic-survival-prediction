# dashboard/app.py

import streamlit as st
import requests
import json

# --- API and Model Information ---

# The address where our v3.1 API runs (running on port 8000 in Docker)
API_URL = "http://localhost:8000/predict"


# --- Streamlit Interface ---

st.set_page_config(
    page_title="Titanic Survival Prediction",
    page_icon="🚢",
    layout="centered"
)

st.title("🚢 Titanic Survival Prediction (v4.0)")
st.markdown("---")
st.write(
    "This is a Streamlit dashboard that consumes a FastAPI backend."
    "The model is running in a separate Docker container."
)

# --- User Input (Input Form) ---
st.header("Enter Passenger Details:")

col1, col2 = st.columns(2)

with col1:
    p_class = st.selectbox("Passenger Class (Pclass)", [1, 2, 3])
    sex = st.selectbox("Sex", ["male", "female"])
    embarked = st.selectbox("Port of Embarkation (Embarked)", ["C", "Q", "S"])

with col2:
    age = st.slider("Age", 0, 100, 25)
    sib_sp = st.number_input("Siblings/Spouses (SibSp)", 0, 10, 0)
    par_ch = st.number_input("Parents/Children (Parch)", 0, 10, 0)


fare = st.slider("Fare", 0.0, 600.0, 32.20)

# --- Prediction Button and API Request ---

if st.button("🚢 Predict Survival"):

    # 1. Convert user input to the JSON format our API expects
    passenger_data = {
        "Pclass": p_class,
        "Sex": sex,
        "Age": age,
        "SibSp": sib_sp,
        "Parch": par_ch,
        "Fare": fare,
        "Embarked": embarked
    }

    try:
        # 2. Send a POST request to FastAPI (http://localhost:8000/predict)
        response = requests.post(API_URL, json=passenger_data)
        response.raise_for_status() # If there is an error (e.g. 500), throw an exception

        # 3. Retrieve JSON response from API
        prediction = response.json()
        survived = prediction.get("Survived")

        # 4. Print the result beautifully on the screen
        if survived == 1:
            st.success("🎉 **This passenger would have SURVIVED!** 🎉")
        else:
            st.error("💔 **This passenger would NOT have survived.** 💔")

    except requests.exceptions.ConnectionError:
        st.error(
            "Connection Error: Could not connect to the API. "
            "Is the v3.1 Docker container running?"
            "\nRun: `docker run -d --rm -p 8000:80 -v ${pwd}/models:/app/models titanic-api:v3`"
        )
    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.json(passenger_data) # Show what we sent on error