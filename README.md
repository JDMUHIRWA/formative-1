# Global Earthquake — FastAPI + ML Prediction

This repository contains a small FastAPI-based service for storing earthquake records and a simple machine learning workflow to predict tsunami occurrence from earthquake data. It includes dataset artifacts, database documentation, and scripts to train and run a model that predicts the `tsunami` target (0/1).

This README describes the project layout, how to run the API, how to train the model, and how to make and store predictions.

---

## Project overview

- API: A FastAPI app exposing CRUD endpoints for `earthquakes` stored in PostgreSQL using SQLAlchemy.
- Data: A CSV dataset with earthquake/tsunami records in `database/dataset/Global Earthquake Tsunami Data.csv`.
- ML: A training script to build a scikit-learn pipeline (imputer → scaler → RandomForest) and a prediction script that fetches the latest earthquake and stores the prediction in an audit log table.

Key design points:
- The API creates tables on startup (uses `models.Base.metadata.create_all`). This is convenient for development but consider adding Alembic migrations for production.
- The ML pipeline is stored with `joblib` as `prediction-model/model.joblib` and the feature list in `prediction-model/model_features.json`.

---

## Repository structure

Top-level folders of interest:

- `api/postgres_version/` — contains the FastAPI service and Python dependencies.
  - `api/postgres_version/main.py` — FastAPI app and endpoints.
  - `api/postgres_version/crud.py` — database helpers (CRUD + `get_latest_earthquake`, `create_audit_log`).

- `database/` — DB-related artifacts
  - `database/dataset/Global Earthquake Tsunami Data.csv` — original dataset used for training.
  - `database/docs/doc.md` — database schema design, stored procedures, triggers and example queries.
  - `database/sql/` — SQL create scripts and triggers (if present).
  - `api/postgres_version/models.py` — SQLAlchemy models (`Earthquake`, `EarthquakeAuditLog`).
  - `api/postgres_version/database.py` — SQLAlchemy engine and SessionLocal (reads `POSTGRES_URL` from `.env`).

- `prediction-model/` — utility scripts
  - `prediction-model/train_model.py` — trains the model and writes `api/app/model.joblib` and `api/app/model_features.json`.
  - `prediction-model/predict_from_latest.py` — fetches `/earthquakes/latest`, loads the model, predicts, and stores a `PREDICT` audit record using `create_audit_log`.

Note: some branches or edits may have the prediction script under `prediction-model/predict_from_latest.py`. Use whichever exists in your branch.

---

## Requirements / Prerequisites

- Python 3.8+ installed.
- PostgreSQL running and reachable.
- A virtual environment is recommended.

Dependencies (install in a virtualenv):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r api/requirements.txt
```

`requirements.txt` contains the API dependencies (FastAPI, uvicorn, SQLAlchemy, python-dotenv, etc.) and the README ensures ML dependencies are present (scikit-learn, pandas, numpy, joblib, requests).

Environment variables

Create a `.env` file in the project root (next to this README) with at least:

```
POSTGRES_SQL=postgresql://<user>:<password>@<host>:<port>/<db>
```

Examples:

```
POSTGRES_SQL=postgresql://postgres:password@localhost:5432/postgres
```

The `database/database.py` file reads `POSTGRES_SQL` via python-dotenv.

---

## Running the API (development)

Start the FastAPI app (from project root):

```powershell
# activate venv first
uvicorn api.app.main:app --reload
```

Open the interactive docs: http://127.0.0.1:8000/docs

Available endpoints (core):

- POST `/earthquakes/` — create a new earthquake record (body: EarthquakeCreate schema)
- GET `/earthquakes/` — list earthquakes (query: skip, limit)
- GET `/earthquakes/{id}` — get a single earthquake
- PUT `/earthquakes/{id}` — update an earthquake
- DELETE `/earthquakes/{id}` — delete an earthquake
- GET `/earthquakes/latest` — returns the most recent earthquake ordered by `earthquake_id` (added for prediction workflow)

The API will create the `earthquakes` and `earthquake_audit_log` tables on startup using SQLAlchemy `create_all` (development behavior).

---

## Training the ML model

The repository includes a training script that builds a simple model to predict the `tsunami` target from the dataset CSV.

Run the trainer from the project root (ensure the dataset exists at `database/dataset/Global Earthquake Tsunami Data.csv`):

```powershell
python scripts/train_model.py
```

What it does
- Reads the CSV and selects features: `magnitude, cdi, mmi, sig, nst, dmin, gap, depth, latitude, longitude, Year, Month`.
- Trains a scikit-learn Pipeline: median imputer → StandardScaler → RandomForestClassifier.
- Evaluates on a holdout set and prints accuracy and a classification report.
- Saves the pipeline to `prediction-model/model.joblib` and the feature list to `prediction-model/model_features.json`.

Notes
- The training script is intentionally simple and intended as a starting point. You may want to expand feature engineering, handle class imbalance, tune hyperparameters, and persist training metadata.

---

## Predicting from the latest record and storing results

After training and with the API running, you can run the prediction script which:

1. Calls `GET /earthquakes/latest` to fetch the most recent earthquake record.
2. Prepares the features expected by the model using the saved feature list.
3. Loads `prediction-model/model.joblib` and predicts the `tsunami` value.
4. Stores a new entry in `earthquake_audit_log` with operation `PREDICT` and `new_values` containing the prediction, predicted probabilities (if available), and feature values.

Run it with:

```powershell
python scripts/predict_from_latest.py
```

If your branch stores the script under `prediction-model/predict_from_latest.py`, run that path instead.

Important: the prediction script uses the running API to fetch the record but writes the audit log directly via the database session (`api.database.SessionLocal`) to ensure consistent audit storage.

---

## Database / Schema notes

- The `database/docs/doc.md` file contains the intended normalized schema (tables for `locations`, `seismic_monitoring`, `tsunami_events`), stored procedures and triggers. The current Python models implement `earthquakes` and an `earthquake_audit_log` table. If you want the full normalized schema, create the additional models and migrations and/or run the SQL scripts under `database/sql/` (if provided).
- For production use prefer Alembic migrations over `create_all`.

---

## Suggestions & next steps

- Add Alembic and create migrations for schema evolution.
- Implement API authentication and authorization if the service will be publicly reachable.
- Add unit tests for the API endpoints (pytest + FastAPI TestClient) and for training/prediction pipelines.
- Improve the ML pipeline: feature engineering (location / monitoring features), hyperparameter tuning, cross-validation, and model evaluation per time-based splits.
- Consider exposing a `/predict` POST endpoint to accept an earthquake record (or id) and return a prediction without using an external script.

---

## Troubleshooting

- `ImportError` / missing packages: ensure you installed `requirements.txt` inside the active virtual environment and that ML packages are installed.
- `Database connection` errors: verify `.env` contains a valid `POSTGRES_SQL` and that Postgres is accessible.
- `Model not found`: run `python scripts/train_model.py` to create `prediction-model/model.joblib`.

---

## Contact / Credits

Created as part of a formative ML pipeline project. For questions or help extending the project, open an issue or contact the maintainer in the repo.
