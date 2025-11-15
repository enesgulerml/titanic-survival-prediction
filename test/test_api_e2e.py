# test/test_api_e2e.py

import pytest
import requests
import subprocess
import time
import os
from pathlib import Path

# === Test Configuration ===
PROJECT_ROOT = Path(__file__).parent.parent
IMAGE_NAME = "titanic-api:v3"  # The v3.0 API image for THIS project
CONTAINER_NAME = "test_titanic_api_service"
API_URL = "http://127.0.0.1:8001"  # Use a different port (8001) to avoid conflicts
HEALTH_CHECK_URL = f"{API_URL}/"
PREDICT_URL = f"{API_URL}/predict"
MODEL_PATH = PROJECT_ROOT / "models"


@pytest.fixture(scope="module")
def api_service():
    """
    pytest Fixture: Manages the lifecycle of the v3.0 Titanic API container.

    1. (Setup) Starts the 'titanic-api:v3' Docker container.
    2. Waits for the Uvicorn server to boot.
    3. 'yield' control back to the test function.
    4. (Teardown) Stops and removes the container.
    """

    # --- Setup ---
    print(f"\n[Setup] Starting v3.0 API Docker container '{IMAGE_NAME}'...")

    model_volume_mount = f"{PROJECT_ROOT.resolve()}/models:/app/models"

    start_command = [
        "docker", "run",
        "-d", "--rm",
        "--name", CONTAINER_NAME,
        "-p", "8001:80",  # Map 8001 (host) to 80 (container)
        "-v", model_volume_mount,
        IMAGE_NAME
    ]

    try:
        subprocess.run(start_command, check=True, capture_output=True)
        print(f"[Setup] Container '{CONTAINER_NAME}' started on port 8001.")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to start Docker container. Is the '{IMAGE_NAME}' "
                    f"image built? Is Docker running? Error: {e.stderr.decode()}")

    # Wait for the Uvicorn server to boot (10 seconds)
    time.sleep(10)

    # --- Health Check ---
    retries = 5
    for i in range(retries):
        try:
            response = requests.get(HEALTH_CHECK_URL, timeout=5)
            if response.status_code == 200:
                print("[Setup] Health check passed. API is live.")
                break
            time.sleep(2)
        except requests.exceptions.ConnectionError:
            if i == retries - 1:
                pytest.fail("E2E Test Failed: Could not connect to the API.")
            time.sleep(2)

    yield PREDICT_URL

    # --- Teardown ---
    print(f"\n[Teardown] Stopping container '{CONTAINER_NAME}'...")
    subprocess.run(["docker", "stop", CONTAINER_NAME], capture_output=True)
    print("[Teardown] Container stopped and removed.")


@pytest.mark.slow
def test_api_predict_endpoint_survives(api_service):
    """
    Test v5.3 (E2E Test):
    Sends a "high-survival-chance" passenger (Rose) to the live API
    and asserts the (expected) "SURVIVED" (1) response.
    """
    # Arrange: Rose DeWitt Bukater (1st Class, Female, 19, Fare 50, Embarked C)
    payload = {
        "Pclass": 1,
        "Sex": "female",
        "Age": 19,
        "SibSp": 1,
        "Parch": 0,
        "Fare": 50.0,
        "Embarked": "C"
    }

    # Act
    response = requests.post(api_service, json=payload)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Survived" in data
    assert data["Survived"] == 1  # Rose should survive


@pytest.mark.slow
def test_api_predict_endpoint_dies(api_service):
    """
    Test v5.3 (E2E Test):
    Sends a "low-survival-chance" passenger (Jack) to the live API
    and asserts the (expected) "DID NOT SURVIVE" (0) response.
    """
    # Arrange: Jack Dawson (3rd Class, Male, 20, Fare 5, Embarked S)
    payload = {
        "Pclass": 3,
        "Sex": "male",
        "Age": 20,
        "SibSp": 0,
        "Parch": 0,
        "Fare": 5.0,
        "Embarked": "S"
    }

    # Act
    response = requests.post(api_service, json=payload)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Survived" in data
    assert data["Survived"] == 0  # Jack should not survive (in this model)