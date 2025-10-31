"""Fetch latest earthquake via the new API endpoint, prepare features, load model, predict, and store prediction in earthquake audit log.

Run with project root on PYTHONPATH so `api.app` can be imported, e.g.:
    python prediction-model/predict_from_latest.py

Requirements: requests, joblib, pandas. The script will use the DB session from `api.app.database` and `api.app.crud.create_audit_log` to store the result.
"""
import json
import requests
from pathlib import Path
from pprint import pprint

# import DB/session and crud from the app
from api.app import database, crud
from api.app.database import SessionLocal

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "api" / "app" / "model.joblib"
FEATURES_PATH = ROOT / "api" / "app" / "model_features.json"
API_BASE = "http://127.0.0.1:8000"

import joblib
import pandas as pd


def fetch_latest():
    url = f"{API_BASE}/earthquakes/latest"
    r = requests.get(url)
    r.raise_for_status()
    return r.json()


def prepare_features(record, features):
    # record is expected to have keys matching the feature names
    data = {f: record.get(f) for f in features}
    df = pd.DataFrame([data])
    return df


def main():
    if not MODEL_PATH.exists():
        raise SystemExit(f"Model not found at {MODEL_PATH}. Run scripts/train_model.py first.")

    model = joblib.load(MODEL_PATH)

    with open(FEATURES_PATH, "r", encoding="utf-8") as f:
        features = json.load(f)["features"]

    print("Fetching latest earthquake from API...")
    record = fetch_latest()
    pprint(record)

    X = prepare_features(record, features)

    pred = model.predict(X)[0]
    proba = None
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(X)[0].tolist()

    result = {"prediction": int(pred), "probability": proba}

    # store in DB audit log
    db = SessionLocal()
    try:
        new_values = {"prediction": int(pred)}
        if proba is not None:
            new_values["probability"] = proba
        new_values["features"] = X.to_dict(orient="records")[0]

        log = crud.create_audit_log(
            db=db,
            table_name="earthquakes",
            operation="PREDICT",
            record_id=record.get("earthquake_id"),
            old_values=None,
            new_values=new_values,
            changed_by="predict_from_latest.py",
        )
        print("Stored audit log:")
        pprint({"log_id": log.log_id, "new_values": log.new_values})
    finally:
        db.close()

    print("Prediction result:", result)


if __name__ == "__main__":
    main()
