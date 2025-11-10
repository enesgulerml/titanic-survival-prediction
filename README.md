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

---

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