# app.py

import streamlit as st
import pandas as pd
import joblib
from src.extract_features import extract_features
from src.entropy_engine import estimate_crack_time


MODEL_PATH = "models/model.pkl"

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

def generate_feedback(features):
    feedback = []

    if features["length"] < 10:
        feedback.append("🔹 Password is quite short — aim for 12+ characters.")

    if features["entropy"] < 35:
        feedback.append("🔹 Entropy is low — try using more unique characters.")

    if features["has_common_pattern"]:
        feedback.append("🔹 Avoid common patterns like '123', 'password', or 'qwerty'.")

    if features["has_keyboard_pattern"]:
        feedback.append("🔹 Avoid keyboard patterns like 'asdf' or 'zxcvbn'.")

    if features["variation_score"] < 0.5:
        feedback.append("🔹 Increase character variety — avoid repeated or similar characters.")

    if features["is_dictionary_word"]:
        feedback.append("🔹 Don’t use dictionary words — try combining random words or symbols.")

    if not feedback:
        feedback.append("🔹 Consider increasing length or adding more complexity just to be safe.")

    return feedback


def main():
    st.set_page_config(page_title="Password Strength Estimator", layout="centered")
    st.title("🔐 Password Strength Estimator")
    st.markdown("Enter a password below to evaluate its strength using a trained AI model.")

    model = load_model()
    password = st.text_input("🔑 Enter your password", type="password")

    if password:
        features = extract_features(password)
        entropy = features["entropy"]
        crack_time = estimate_crack_time(entropy)
        X = pd.DataFrame([features])
        prediction = model.predict(X)[0]
        proba = model.predict_proba(X)[0][prediction]

        label_map = {
            0: "🔴 Weak",
            1: "🟠 Medium",
            2: "🟢 Strong"
        }
        strength_label = label_map.get(prediction, "❓ Unknown")

        st.markdown(f"### Prediction: {strength_label}")
        st.markdown(f"**Confidence:** {proba:.2%}")
        st.markdown(f"🧠 Adjusted Entropy: `{features['entropy']:.2f}` bits")
        st.markdown(f"📉 Raw Entropy: `{features['raw_entropy']:.2f}` bits")
        st.markdown(f"🏷️ Entropy Score (0–4): `{features['entropy_score']}`")
        st.markdown(f"⏱️ Crack Time (offline GPU): **{estimate_crack_time(features['entropy'], attack_mode='gpu')}**")


        with st.expander("📊 View Extracted Features"):
            st.json(features)

        if prediction == 0:
            st.warning("💡 Your password may be weak. Suggestions:")
            feedback = generate_feedback(features)
            for item in feedback:
                st.markdown(f"- {item}")

if __name__ == "__main__":
    main()
