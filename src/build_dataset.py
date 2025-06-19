# src/build_dataset.py

import pandas as pd
import random
import string
from src.extract_features import extract_features

# Load weak passwords (leaked ones from rockyou.txt)
def load_weak_passwords(path, limit=50000):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    return [line.strip() for line in lines if line.strip()][:limit]

# Generate medium-strength passwords
def generate_medium_passwords(n=50000):
    base = [
        "Welcome2024",
        "SecureHome1",
        "Password123!",
        "Sunshine99",
        "MyLogin!23",
        "Winter2023!",
        "QwertyUiop1",
        "August@2023",
        "FitnessGoals9",
        "DogsAreCool123"
    ]
    passwords = []
    for _ in range(n):
        pwd = random.choice(base)
        mutations = [
            lambda x: x + "!",
            lambda x: x.lower(),
            lambda x: x + str(random.randint(10, 99)),
            lambda x: x.replace("o", "0").replace("i", "1"),
            lambda x: x[::-1],
        ]
        passwords.append(random.choice(mutations)(pwd))
    return passwords

# Generate strong passwords
def generate_strong_passwords(n=50000, min_len=12, max_len=24):
    charset = string.ascii_letters + string.digits + string.punctuation
    return [
        ''.join(random.choices(charset, k=random.randint(min_len, max_len)))
        for _ in range(n)
    ]

# Build labeled dataset
def build_dataset():
    weak_pwds = load_weak_passwords("data/rockyou.txt", limit=50000)
    medium_pwds = generate_medium_passwords(n=50000)
    strong_pwds = generate_strong_passwords(n=50000)

    all_features = []
    for pwd in weak_pwds:
        features = extract_features(pwd)
        features['label'] = 0  # Weak
        all_features.append(features)
    
    # Add medium passwords
    for pwd in medium_pwds:
        features = extract_features(pwd)
        features['label'] = 1
        all_features.append(features)

    for pwd in strong_pwds:
        features = extract_features(pwd)
        features['label'] = 2  # Strong
        all_features.append(features)

    df = pd.DataFrame(all_features)
    df.to_csv("data/dataset.csv", index=False)
    print("✅ Dataset saved to data/dataset.csv")

if __name__ == "__main__":
    build_dataset()
