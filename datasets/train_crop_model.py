"""
datasets/train_crop_model.py

Trains a RandomForest classifier on the Crop Recommendation Dataset and
saves the model + label encoder to datasets/crop/.

Usage:
    python datasets/train_crop_model.py

Dataset source: https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset
Place the CSV at: datasets/crop/Crop_recommendation.csv
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_OUT_DIR = Path(__file__).parent / "crop"
_CSV     = _OUT_DIR / "Crop_recommendation.csv"


def train() -> None:
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelEncoder
    from sklearn.metrics import accuracy_score
    import joblib

    if not _CSV.exists():
        print(f"❌  Dataset not found: {_CSV}")
        print("    Download from Kaggle and place it at datasets/crop/Crop_recommendation.csv")
        sys.exit(1)

    print("Loading dataset...")
    df = pd.read_csv(_CSV)

    features = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
    X = df[features].values
    y_raw = df["label"].values

    # Encode labels to integers
    le = LabelEncoder()
    y  = le.fit_transform(y_raw)
    labels: list = le.classes_.tolist()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("Training RandomForest classifier...")
    clf = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
    clf.fit(X_train, y_train)

    acc = accuracy_score(y_test, clf.predict(X_test))
    print(f"Accuracy: {acc * 100:.2f}%")

    # Save model and labels
    _OUT_DIR.mkdir(parents=True, exist_ok=True)
    model_path  = _OUT_DIR / "crop_model.joblib"
    labels_path = _OUT_DIR / "crop_labels.json"

    joblib.dump(clf, model_path)
    labels_path.write_text(json.dumps(labels))

    print(f"Model saved  -> {model_path}")
    print(f"Labels saved -> {labels_path}")


if __name__ == "__main__":
    train()
