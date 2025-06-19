# 🔐 Password Strength Estimator (AI-Powered)

A machine learning–powered password strength evaluation tool that analyzes passwords using real-world leak data, entropy models, and modern prediction techniques. Includes a clean Streamlit interface and custom crack-time estimation engine.

---

## 🚀 Features

- ✅ AI-powered strength classification (Weak / Medium / Strong)
- ✅ Trained on real leaked password data (RockYou, etc.)
- ✅ Entropy-based scoring with pattern-aware penalty system
- ✅ Estimated crack time (offline GPU, online, and dictionary attacks)
- ✅ Streamlit web app frontend
- ✅ Modular feature extraction pipeline (easy to extend)
- ✅ Leetspeak, repetition, sequence, dictionary-word detection
- ✅ No hardcoded rules — dynamically builds weak word bases from data

---

## 🧠 How It Works

1. **Feature Extraction**: Passwords are transformed into a rich set of features (length, variation, repetition, entropy, etc.)
2. **Model Training**: A Random Forest classifier is trained using labeled password strength categories
3. **Prediction**: The model outputs a strength class and confidence score
4. **Entropy Engine**: Adjusted entropy and estimated crack time are calculated using real-world heuristics

---

## 🛠️ Setup

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/password-strength-estimator.git
cd password-strength-estimator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install requirements
pip install -r requirements.txt

# Build dataset and train model
python -m src.build_dataset
python -m src.train_model

# Predict via CLI
python -m src.predict 'MyPassword123!'
🌐 Run Web App
streamlit run app.py
Then open http://localhost:8501 in your browser.
```
---

## 📂 Project Structure
.
├── app.py                  # Streamlit interface
├── requirements.txt
├── README.md
├── data/                   # RockYou, wordlists, etc.
├── models/                 # Trained model .pkl
└── src/
    ├── build_dataset.py
    ├── train_model.py
    ├── predict.py
    ├── extract_features.py
    ├── entropy_engine.py
    └── common_bases.py
---

## 📄 License
MIT License — feel free to use and adapt this project.

---

## 🙏 Credits
- RockYou dataset

- SecLists by Daniel Miessler

- Streamlit

- Scikit-learn

- NumPy
s
- Pandas