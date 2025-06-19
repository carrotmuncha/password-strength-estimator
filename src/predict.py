# src/predict.py

import joblib
import sys
import pandas as pd
from src.extract_features import extract_features
from src.entropy_engine import estimate_crack_time

MODEL_PATH = "models/model.pkl"

label_map = {
    0: "🔴 Weak",
    1: "🟠 Medium",
    2: "🟢 Strong"
}

def predict_strength(password):
    try:
        model = joblib.load(MODEL_PATH)
    except FileNotFoundError:
        print(f"❌ Model not found at {MODEL_PATH}. Please train the model first.")
        return

    features = extract_features(password)
    X = pd.DataFrame([features])
    prediction = model.predict(X)[0]
    prob = model.predict_proba(X)[0][prediction]

    print(f"\n🔐 Password: '{password}'")
    print(f"📊 Prediction: {label_map[prediction]} (confidence: {prob:.2f})")
    print(f"🧠 Adjusted Entropy: {features['entropy']:.2f} bits")
    print(f"📉 Raw Entropy: {features['raw_entropy']:.2f} bits")
    print(f"🏷️ Entropy Score (0-4): {features['entropy_score']}")
    print(f"⏱️ Estimated Crack Time (GPU): {estimate_crack_time(features['entropy'], attack_mode='gpu')}\n")

if __name__ == "__main__" :
    if len(sys.argv) != 2:
        print("Usage: python -m src.predict '<password>'")
    else:
        predict_strength(sys.argv[1])