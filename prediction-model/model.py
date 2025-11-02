"""Train a tsunami prediction model and save it to `prediction-model/model.joblib`.

This script:
- Loads the CSV dataset in `database/dataset/Global Earthquake Tsunami Data.csv`
- Trains a simple scikit-learn pipeline (imputer -> scaler -> classifier)
- Evaluates and prints a basic accuracy on a holdout split
- Saves the trained pipeline and a feature list to `prediction-model/model.joblib` and `prediction-model/model_features.json`

Run from project root with the virtualenv active.
"""
from pathlib import Path
import json
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "database" / "dataset" / "Global Earthquake Tsunami Data.csv"
MODEL_OUT = ROOT / "prediction-model" / "model.joblib"
FEATURES_OUT = ROOT / "prediction-model" / "model_features.json"

if __name__ == "__main__":
    print("Loading dataset:", DATA_PATH)
    df = pd.read_csv(DATA_PATH)
    # target: 'tsunami' (0/1)
    target = "tsunami"

    # choose features available in both CSV and API model fields
    features = [
        "magnitude",
        "cdi",
        "mmi",
        "sig",
        "nst",
        "dmin",
        "gap",
        "depth",
        "latitude",
        "longitude",
        "Year",
        "Month",
    ]

    # keep only chosen columns and drop rows where target is missing
    df = df[features + [target]].copy()
    df = df.dropna(subset=[target])

    X = df[features]
    y = df[target].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
        ("clf", RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)),
    ])

    print("Training model...")
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Test accuracy: {acc:.4f}")
    print(classification_report(y_test, y_pred))

    MODEL_OUT.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_OUT)
    print("Saved model to", MODEL_OUT)

    with open(FEATURES_OUT, "w", encoding="utf-8") as f:
        json.dump({"features": features}, f)
    print("Saved feature list to", FEATURES_OUT)