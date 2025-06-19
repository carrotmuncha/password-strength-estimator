# src/train_model.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import os

def train_model():
    # Load dataset
    df = pd.read_csv("data/dataset.csv")
    X = df.drop("label", axis=1)
    y = df["label"]

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Train Random Forest
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    print("✅ Classification Report:")
    print(classification_report(y_test, y_pred))
    print("📊 Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    # Save model
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/model.pkl")
    print("💾 Model saved to models/model.pkl")

if __name__ == "__main__":
    train_model()
