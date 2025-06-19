# src/entropy_engine.py

import numpy as np
import re
import math

from src.common_bases import build_common_bases

COMMON_BASES = build_common_bases(
    leak_path="data/rockyou.txt",
    limit=10000,
    min_word_len=4,
    alpha_only=True,
    extra=True
)

try:
    with open("data/wordlist.txt") as f:
        DICTIONARY_WORDS = set(w.strip().lower() for w in f if len(w.strip()) > 3)
except FileNotFoundError:
    DICTIONARY_WORDS = set()

# Realistic charset breakdown
def refined_charset_size(password):
    sets = [
        any(c.islower() for c in password),
        any(c.isupper() for c in password),
        any(c.isdigit() for c in password),
        any(c in "!@#$%^&*()-_=+[]{};:'\",.<>/?\\|`~" for c in password)
    ]
    sizes = [26, 26, 10, 33]
    return sum(size for flag, size in zip(sets, sizes) if flag)

# Pattern penalties for common bad structures
def pattern_penalty(password):
    penalty = 0

    if len(password) < 8:
        penalty += 10  # short length

    if re.search(r'(abc|123|qwe|asdf|zxcv)', password.lower()):
        penalty += 5

    if re.search(r'(.)\1{2,}', password):  # e.g., aaa, 1111
        penalty += 5

    if re.search(r'(19|20)\d{2}', password):  # common years
        penalty += 10   

    if any(base in password.lower() for base in COMMON_BASES):
        penalty += 20

    if re.match(r'^[A-Z][a-z]+[\d\W]{1,4}$', password):
        penalty += 15  # e.g., "Welcome2023!", classic pattern

    if password.isdigit() or password.isalpha():
        penalty += 10  # single-type passwords
    
    if password.lower() in DICTIONARY_WORDS:
        penalty += 10

    return penalty

# Calculate raw + adjusted entropy
def calculate_entropy(password):
    if not password:
        return 0.0, 0.0

    charset = refined_charset_size(password)
    raw_entropy = len(password) * np.log2(charset + 1)  # +1 to avoid log2(0)

    penalty = pattern_penalty(password)
    adjusted_entropy = max(raw_entropy - penalty, 0)

    return round(raw_entropy, 2), round(adjusted_entropy, 2)

# Crack time estimation based on entropy + attack mode
def estimate_crack_time(entropy, attack_mode="offline"):
    guesses_per_second = {
        "online": 1e2,
        "offline": 1e9,
        "gpu": 1e12
    }.get(attack_mode, 1e9)

    guesses = 2 ** entropy
    seconds = guesses / guesses_per_second

    if seconds < 1:
        return "🧨 Instantly cracked"
    elif seconds < 60:
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:
        return f"{seconds / 60:.2f} minutes"
    elif seconds < 86400:
        return f"{seconds / 3600:.2f} hours"
    elif seconds < 2592000:
        return f"{seconds / 86400:.2f} days"
    elif seconds < 31536000:
        return f"{seconds / 2592000:.2f} months"
    else:
        return f"{seconds / 31536000:.2f} years"


def score_entropy(entropy):
    if entropy < 20:
        return 0  # Very Weak
    elif entropy < 30:
        return 1  # Weak
    elif entropy < 40:
        return 2  # Medium
    elif entropy < 60:
        return 3  # Strong
    else:
        return 4  # Very Strong
