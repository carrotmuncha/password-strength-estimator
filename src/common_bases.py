import re

def generate_keywords():
    return (
        generate_months() +
        generate_seasons() +
        generate_keyboard_patterns() +
        generate_simple_names() +
        generate_popculture_terms() +
        generate_common_tech_words()
    )

def generate_months():
    return [m.lower() for m in [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]]

def generate_seasons():
    return ["spring", "summer", "autumn", "fall", "winter"]

def generate_keyboard_patterns():
    return ["qwerty", "asdf", "zxcvbn", "qazwsx"]

def generate_simple_names():
    return ["michael", "jessica", "daniel", "jordan", "ashley", "andrew", "robert", "john", "david", "thomas"]

def generate_popculture_terms():
    return ["pokemon", "batman", "superman", "harry", "hogwarts", "matrix", "starwars", "marvel", "ironman"]

def generate_common_tech_words():
    return ["admin", "root", "test", "default", "debug", "login"]

def build_common_bases(
    leak_path="data/rockyou.txt",
    limit=10000,
    min_word_len=4,
    alpha_only=True,
    extra=True
):
    base_words = set()

    # 1. Extract leaked passwords
    try:
        with open(leak_path, "r", encoding="utf-8", errors="ignore") as f:
            for i, line in enumerate(f):
                if i >= limit:
                    break
                word = line.strip().lower()
                if len(word) < min_word_len:
                    continue
                if alpha_only and not word.isalpha():
                    continue
                base_words.add(word)
    except FileNotFoundError:
        pass

    # 2. Add structured extras (e.g., months, tech terms, names)
    if extra:
        base_words.update(generate_keywords())

    return sorted(base_words)
