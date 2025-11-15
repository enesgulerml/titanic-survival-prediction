# End-to-End Titanic Survival Prediction (v1.0)

This project is an end-to-end machine learning pipeline built to predict passenger survival on the Titanic, based on the classic Kaggle dataset.

The primary goal is not just to build a model, but to engineer a professional, reproducible, and scalable project structure. This codebase moves beyond monolithic notebooks into a "Google-level" production-ready format that emphasizes:
* **Modularity:** Separating code into distinct, responsible components (`src`).
* **Configuration:** Managing all settings and paths from a central `config.py`.
* **Reproducibility:** Using `conda` for environment management and `pathlib` for path independence.
* **Packaging:** Treating the project's code as an installable Python package (`setup.py`).

---

## 🚀 Project Structure

The repository is organized based on professional data science standards to ensure separation of concerns:

```
titanic-survival-prediction/
│
├── data/
│   └── raw/
│       ├── train.csv         <- (Raw training data, *not* tracked by Git)
│       └── test.csv          <- (Raw prediction data, *not* tracked by Git)
│
├── models/
│   └── titanic_model.joblib  <- (Final trained pipeline, *not* tracked by Git)
│
├── notebooks/
│   └── 01-data-exploration.ipynb <- (EDA and prototyping notebook)
│
├── reports/
│   └── submission.csv        <- (Generated predictions file)
│
├── src/                      <- (All project source code)
│   │
│   ├── __init__.py
│   ├── config.py             <- (All settings, parameters, and file paths)
│   ├── data_processing.py    <- (Data loading and splitting functions)
│   ├── pipeline.py           <- (Scikit-learn pipeline definitions)
│   ├── train.py              <- (Main training script)
│   └── predict.py            <- (Main prediction script)
│
├── .gitignore                <- (Tells Git which files to ignore)
├── environment.yml           <- (Conda environment dependencies)
├── setup.py                  <- (Makes the 'src' folder an installable package)
└── README.md                 <- (This file - The project user manual)
```

---

## 🛠️ Installation & Setup

Follow these steps to set up the project environment on your local machine.

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/enesgulerml/titanic-survival-prediction.git](https://github.com/enesgulerml/titanic-survival-prediction.git)
    cd titanic-survival-prediction
    ```

2.  **Download the Data:**
    This project respects the "Data is not Code" principle. The raw data is ignored by Git (`.gitignore`).
    * Go to the [Kaggle Titanic Competition Data Page](https://www.kaggle.com/c/titanic/data).
    * Download `train.csv` and `test.csv`.
    * Place both files inside the `data/raw/` directory.

3.  **Create Conda Environment:**
    This command reads the `environment.yml` file to create an isolated environment with all necessary libraries.
    ```bash
    conda env create -f environment.yml
    conda activate titanic-survival-prediction
    ```

4.  **Install the Project Package:**
    This is the crucial step that makes your `src` code importable. The `-e` (editable) flag links your environment to your source code directly.
    ```bash
    pip install -e .
    ```
    **Note:** If you encounter environment-specific errors (like conda not found or docker memory issues), please check our TROUBLESHOOTING.md guide.

---

## 🧪 v5.1: Running Automated Tests (Pytest)

This project includes a "safety net" of automated unit tests using `pytest` located in the `test/` directory. These tests verify the integrity of the core components (like the model pipeline).

After installation (Step 4), you can run all tests from the project root directory:

```bash
python -m pytest
```

If all tests pass (`3 passed`), the project's core logic is confirmed to be working as expected.

## ⚡ How to Use

Once installed, the project provides two main functions via the command line.

### 1. To Train the Model

This script will load the raw data, run it through the `scikit-learn` pipeline, train the model, evaluate it, and save the final pipeline object to the `models/` directory.

```bash
python -m src.train
```

You will see the following output upon success:
```
===== Training Process Has Been Completed =====
...
The accuracy score of the model on the test data: 0.8212
...
The model has been successfully saved.
===== Training Process Has Been Completed =====
```

### 2. To Generate Predictions

This script will load your saved model from `models/`, run the `data/raw/test.csv` file through it, and save the final predictions to the `reports/` directory.

```bash
python -m src.predict
```

The resulting `reports/submission.csv` file is formatted and ready to be submitted to the Kaggle competition.

---

## 🔬 v2.0: Experiment Tracking (MLFlow)

This project is integrated with **MLFlow** to log, track, and compare different training runs.

### 1. View the Experiment Dashboard

After running the training script (`python -m src.train`), MLFlow logs are saved locally to the `mlruns/` directory (which is ignored by Git).

To launch the MLFlow web dashboard, run the following command from your project root directory:

```bash
mlflow ui
```

This will launch a server (usually at `http://127.0.0.1:5000`) where you can see all parameters, metrics (`accuracy`), and saved model artifacts for every run.

### 2. Run Training (MLFlow-enabled)

The `src.train` script is now wrapped with MLFlow. Every time you run it, a new "Run" will be logged in the MLFlow UI.

```bash
python -m src.train
```

---

## 📦 v2.1: Portability (Docker)

This project includes a `Dockerfile` and `.dockerignore` to build a portable, self-contained container image of the v2.0 application.

The core principle is **"Code in Image, Data on Volume."**
* The **Image** (`titanic-service:v2`) contains only the `conda` environment and the `src` code.
* The **Volumes** (`data/`, `models/`, `mlruns/`) are mounted from your host machine at runtime.

### 1. Build the Docker Image

From the project root directory, run:

```bash
docker build -t titanic-service:v2 .
```

### 2. Run Training Inside Docker (with Volume Mounts)

This command runs the training script *inside* the container, but mounts your local `data`, `models`, and `mlruns` folders. This ensures that the data is read correctly and the resulting model/logs are saved *back to your host machine*.

```bash
docker run --rm \
  -v ${pwd}/data:/app/data \
  -v ${pwd}/models:/app/models \
  -v ${pwd}/mlruns:/app/mlruns \
  titanic-service:v2 python -m src.train
```

### 3. Run Predictions Inside Docker

Similarly, you can run the batch prediction script inside the container:

```bash
docker run --rm \
  -v ${pwd}/data:/app/data \
  -v ${pwd}/models:/app/models \
  -v ${pwd}/reports:/app/reports \
  titanic-service:v2 python -m src.predict
```

---

## 🚀 v3.0: API Serving (FastAPI & Docker)

This project includes a **v3.0** upgrade that wraps the trained model (v2.1) into a production-ready API server using **FastAPI**.

This API (the "Motor") is decoupled from any frontend. It is designed to be consumed by other machines or services (like a Streamlit dashboard, a mobile app, or another backend).

The API provides:
* **Automatic Data Validation** via Pydantic (`app/schema.py`).
* **Automatic API Documentation** via Swagger UI (`/docs`).

### 1. Build the v3.0 API Image

This `Dockerfile` is optimized for production. It copies the `src` and `app` packages, and the `CMD` starts the `uvicorn` server automatically on port 80.

```bash
docker build -t titanic-api:v3 .
```

### 2. Run the API Server (Docker)

This command runs the API server in "detached" mode (`-d`), maps your local port `8000` to the container's port `80` (`-p 8000:80`), and crucially, mounts the `models/` directory (`-v`) so the API can load the `titanic_model.joblib` file.

```bash
docker run -d --rm \
  -p 8000:80 \
  -v ${pwd}/models:/app/models \
  titanic-api:v3
```

### 3. Test the API

Once the container is running, go to your browser:

* **API Docs (Swagger):** `http://localhost:8000/docs`
* **Health Check:** `http://localhost:8000/`

You can now use the `/docs` interface to send test data (e.g., a single passenger JSON) and get a live prediction (`{"Survived": 1}`).

---

## 🎨 v4.0: Interactive Dashboard (Streamlit)

This repository also includes a v4.0 interactive dashboard powered by **Streamlit**.

This dashboard (`dashboard/app.py`) is a "dumb" client. It demonstrates a key MLOps principle: **decoupling the frontend (UI) from the backend (API).**

This Streamlit app:
* **Does NOT** load the `.joblib` model.
* **Does NOT** import the `src` package.
* **DOES** simply make an HTTP request to the v3.1 FastAPI container (`http://localhost:8000/predict`).

### How to Run the Dashboard

This requires **two separate terminals** running simultaneously:

**➡️ Terminal 1: Run the API Server (v3.1)**
(If not already running) Start the FastAPI Docker container. This is the "Motor".
```bash
docker run -d --rm \
  -p 8000:80 \
  -v ${pwd}/models:/app/models \
  titanic-api:v3
```

**➡️ Terminal 2: Run the Streamlit App (v4.0)**
Activate the conda environment and run the Streamlit app. This is the "Dashboard".
```bash
conda activate titanic-survival-prediction
python -m streamlit run dashboard/app.py
```

Your browser should automatically open to `http://localhost:8501`. You can now interact with the UI, which will send live requests to the API running in Docker.