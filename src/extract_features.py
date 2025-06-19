# src/extract_features.py
import re
import numpy as np

from src.entropy_engine import calculate_entropy, score_entropy

try:
    with open("data/wordlist.txt") as f:
        DICTIONARY_WORDS = set(w.strip().lower() for w in f if len(w.strip()) > 3)
except FileNotFoundError:
    DICTIONARY_WORDS = set()

def extract_features(password):
    length = len(password)
    upper = sum(1 for c in password if c.isupper())
    lower = sum(1 for c in password if c.islower())
    digits = sum(1 for c in password if c.isdigit())
    symbols = sum(1 for c in password if not c.isalnum())
    raw_entropy, adjusted_entropy = calculate_entropy(password)

    has_common_pattern = int(bool(re.search(r'(123|abc|password|qwerty|letmein)', password.lower())))
    has_keyboard_pattern = int(any(p in password.lower() for p in ['qwerty', 'asdf', 'zxcvbn', '1234', '1111', 'abcd']))
    variation_score = round(len(set(password)) / length, 2) if length > 0 else 0
    starts_or_ends_with_simple = int(bool(re.match(r'^[A-Z].*\d$|^\d.*[A-Z]$', password)))
    is_dictionary_word = int(password.lower() in DICTIONARY_WORDS)
    has_leetspeak = int(bool(re.search(r'[4301@$]+', password)))

    return {
        'length': length,
        'upper': upper,
        'lower': lower,
        'digits': digits,
        'symbols': symbols,
        'entropy': adjusted_entropy,
        'raw_entropy': raw_entropy,
        'entropy_score': score_entropy(adjusted_entropy),
        'has_common_pattern': has_common_pattern,
        'has_keyboard_pattern': has_keyboard_pattern,
        'variation_score': variation_score,
        'starts_or_ends_with_simple': starts_or_ends_with_simple,
        'is_dictionary_word': is_dictionary_word,
        'has_leetspeak': has_leetspeak,
        'has_year': has_year(password),
        'caps_start_digit_end': caps_start_digit_end(password),
        'has_sequence': has_sequence(password),
        'has_repetition': has_repetition(password),

    }

def has_year(password):
    return int(bool(re.search(r'(19|20)\d{2}', password)))

def caps_start_digit_end(password):
    return int(bool(re.match(r'^[A-Z].*[\d\W]$', password)))

def has_sequence(password):
    return int(bool(re.search(r'(abc|123|qwe|asdf)', password.lower())))

def has_repetition(password):
    return int(bool(re.search(r'(.)\1{2,}', password)))


if __name__ == "__main__":
    pwd = "P@ssw0rd123"
    print(f"Features for '{pwd}':\n{extract_features(pwd)}")
