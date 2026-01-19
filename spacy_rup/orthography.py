"""
Aromanian Orthography Conversion Utilities

This module provides functions to convert between different Aromanian writing standards:

1. DIARO (Caragiu-Marioțeanu standard):
   - Central vowels: ă, â, î
   - Consonants: d̦ (dz), ľ (palatal l), ń (palatal n), ș, ț

2. Cunia (Tiberiu Cunia standard):
   - Central vowel: ã (unified)
   - Consonant digraphs: dz, lj, nj, sh, ts

3. Other variants:
   - Wikipedia-style with apostrophe: l'
   - Greek-based transcription
   - Various legacy encodings

Usage:
    from orthography import cunia_to_diaro, diaro_to_cunia, normalize_text
    
    # Convert from Cunia to DIARO
    text_diaro = cunia_to_diaro("Bunã dzua!")  # Returns "Bună dzua!"
    
    # Convert from DIARO to Cunia  
    text_cunia = diaro_to_cunia("Bună dzua!")  # Returns "Bunã dzua!"
    
    # Normalize any input to a standard form
    normalized = normalize_text(text, target="cunia")

Based on conversion scripts from:
- https://github.com/arotranslate/AroTranslate/blob/main/deployment/utils/text_processing.py
- https://github.com/senisioi/aromanian/blob/main/scripts/book2DIARO.py
"""

import re
import json
import pickle
from pathlib import Path

# Try to import sklearn components needed for unpickling
try:
    from sklearn.pipeline import Pipeline
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.naive_bayes import MultinomialNB
except ImportError:
    pass


CUNIA_TO_DIARO_CONSONANTS = {
    "sh": "ș",
    "Sh": "Ș",
    "SH": "Ș",
    "ts": "ț",
    "Ts": "Ț",
    "TS": "Ț",
    "lj": "ľ",
    "Lj": "Ľ",
    "LJ": "Ľ",
    "nj": "ń",
    "Nj": "Ń",
    "NJ": "Ń",
    "dz": "d̦",
    "Dz": "D̦",
    "DZ": "D̦",
}

DIARO_TO_CUNIA_CONSONANTS = {
    "ș": "sh",
    "Ș": "Sh",
    "ş": "sh",
    "Ş": "Sh",
    "ț": "ts",
    "Ț": "Ts",
    "ţ": "ts",
    "Ţ": "Ts",
    "ľ": "lj",
    "Ľ": "Lj",
    "l'": "lj",
    "L'": "Lj",
    "l'": "lj",
    "L'": "Lj",
    "ń": "nj",
    "Ń": "Nj",
    "ñ": "nj",
    "Ñ": "Nj",
    "n'": "nj",
    "N'": "Nj",
    "d̦": "dz",
    "D̦": "Dz",
    "ḑ": "dz",
    "Ḑ": "Dz",
    "ḍ": "dz",
    "Ḍ": "Dz",
}

VOWELS_TO_CUNIA = {
    "ă": "ã",
    "Ă": "ã",
    "â": "ã",
    "Â": "ã",
    "î": "ã",
    "Î": "ã",
    "ӑ": "ã",
    "Ӑ": "ã",
    "ǎ": "ã",
    "Ǎ": "ã",
}

OTHER_CHARS = {
    "ŭ": "u",
    "ς": "c",
    "é": "e",
    "í": "i",
    "ū": "u",
    "ì": "i",
    "ā": "a",
    "ĭ": "i",
    "γ": "y",
    "Γ": "Y",
    "ï": "i",
    "ó": "o",
    "θ": "th",
    "Θ": "Th",
    "δ": "dh",
    "Δ": "Dh",
    "á": "a",
    "à": "a",
    "Á": "A",
    "À": "A",
}


def convert_consonants_to_cunia(text: str) -> str:
    """Convert DIARO consonants to Cunia digraphs."""
    for diaro, cunia in DIARO_TO_CUNIA_CONSONANTS.items():
        text = text.replace(diaro, cunia)
    return text


def convert_consonants_to_diaro(text: str) -> str:
    """Convert Cunia digraphs to DIARO consonants."""
    for cunia, diaro in CUNIA_TO_DIARO_CONSONANTS.items():
        text = text.replace(cunia, diaro)
    return text


def convert_vowels_to_cunia(text: str) -> str:
    """Convert all central vowel variants to Cunia ã."""
    for vowel, cunia in VOWELS_TO_CUNIA.items():
        text = text.replace(vowel, cunia)
    return text


def normalize_other_chars(text: str) -> str:
    """Normalize Greek letters and accented characters."""
    for char, norm in OTHER_CHARS.items():
        text = text.replace(char, norm)
    return text


def to_cunia(text: str) -> str:
    """Convert text to Cunia orthography (ã/dz/lj/nj/sh/ts).
    
    Args:
        text: Input text in any Aromanian orthography
        
    Returns:
        Text converted to Cunia standard
    """
    text = convert_consonants_to_cunia(text)
    text = convert_vowels_to_cunia(text)
    text = normalize_other_chars(text)
    return text


from typing import Optional


def resolve_central_vowel_to_diaro(word: str, position: int, fah: Optional[dict] = None, fuh: Optional[dict] = None) -> str:
    """Resolve Cunia ã to DIARO ă or â based on context.
    
    In DIARO standard:
    - î is used at the beginning of words
    - â is used in the middle of words (like Romanian)
    - ă represents schwa /ə/
    
    This uses n-gram frequency data to make the decision when available.
    
    Args:
        word: The word containing ã
        position: Position of ã in the word
        fah: Frequency dictionary for â contexts
        fuh: Frequency dictionary for ă contexts
        
    Returns:
        Either 'î', 'â', or 'ă' depending on position and context
    """
    if position == 0:
        return "î"
    
    if fah and fuh:
        start = max(0, position - 2)
        end = min(len(word), position + 3)
        context = word[start:end].lower()
        
        cnt_ah = fah.get(context, 0)
        cnt_uh = fuh.get(context, 0)
        
        if cnt_ah > cnt_uh:
            return "â"
        else:
            return "ă"
    
    return "ă"



# Valid frequency maps loaded from resources
FREQ_AH = {}
FREQ_UH = {}
ORTHOGRAPHY_MODEL = None

def load_resources():
    """Load n-gram frequency maps and ML model from resources."""
    global FREQ_AH, FREQ_UH, ORTHOGRAPHY_MODEL
    try:
        resource_dir = Path(__file__).parent / "resources"
        ah_path = resource_dir / "freq_ah.json"
        uh_path = resource_dir / "freq_uh.json"
        model_path = resource_dir / "orthography_model.pkl"
        
        if ah_path.exists():
            with open(ah_path, "r", encoding="utf-8") as f:
                FREQ_AH = json.load(f)
                
        if uh_path.exists():
            with open(uh_path, "r", encoding="utf-8") as f:
                FREQ_UH = json.load(f)
        
        if model_path.exists():
            try:
                with open(model_path, 'rb') as f:
                    ORTHOGRAPHY_MODEL = pickle.load(f)
            except (ImportError, ModuleNotFoundError, Exception) as e:
                # If sklearn is not installed or other issue, fail silently and use heuristics
                pass
                
    except Exception as e:
        print(f"Warning: Could not load resources: {e}")
        import traceback
        traceback.print_exc()

# Load on module import
load_resources()

def to_diaro(text: str, fah: Optional[dict] = None, fuh: Optional[dict] = None) -> str:
    """Convert text to DIARO orthography (ăâî/d̦/ľ/ń/ș/ț).
    
    Args:
        text: Input text (ideally already in Cunia for best results)
        fah: Optional n-gram frequency dict for â resolution. Defaults to loaded resources.
        fuh: Optional n-gram frequency dict for ă resolution. Defaults to loaded resources.
        
    Returns:
        Text converted to DIARO standard
    """
    # Use global defaults if not provided
    if fah is None:
        fah = FREQ_AH
    if fuh is None:
        fuh = FREQ_UH

    text = to_cunia(text)
    
    words = []
    current_word = ""
    
    for char in text:
        if char.isalpha() or char == "'":
            current_word += char
        else:
            if current_word:
                words.append(("word", current_word))
                current_word = ""
            words.append(("other", char))
    
    if current_word:
        words.append(("word", current_word))
    
    result = []
    for token_type, token in words:
        if token_type == "word":
            converted = ""
            for i, char in enumerate(token):
                if char.lower() == "ã":
                    new_char = resolve_central_vowel_to_diaro(token.lower(), i, fah, fuh)
                    if char.isupper():
                        new_char = new_char.upper()
                    converted += new_char
                else:
                    converted += char
            converted = convert_consonants_to_diaro(converted)
            result.append(converted)
        else:
            result.append(token)
    
    return "".join(result)


def cunia_to_diaro(text: str) -> str:
    """Convenience function: Convert Cunia to DIARO using best available data.
    
    This is the "Final Translator" that uses n-gram frequency data 
    to correctly resolve 'ã' to 'ă' or 'â'.
    """
    return to_diaro(text)


def diaro_to_cunia(text: str) -> str:
    """Convenience function: Convert DIARO to Cunia."""
    return to_cunia(text)


def detect_orthography(text: str) -> str:
    """Detect which orthographic standard a text uses.
    
    This is the "Aro Model" for detection.
    It uses a trained Naive Bayes classifier if available, otherwise heuristics.
    
    Args:
        text: Input Aromanian text
        
    Returns:
        'cunia', 'diaro', 'mixed', or 'unknown'
    """
    # 1. Try generic heuristics first for obvious cases
    diaro_chars = set("șțăâîľńȘȚĂÂÎĽŃ")
    cunia_patterns = ["sh", "ts", "lj", "nj", "dz"]
    cunia_chars = set("ãÃ")
    
    has_diaro = any(c in diaro_chars for c in text) or "d̦" in text or "D̦" in text
    has_cunia_char = any(c in cunia_chars for c in text)
    has_cunia_pattern = any(p in text.lower() for p in cunia_patterns)
    has_cunia = has_cunia_char or has_cunia_pattern
    
    # 2. Use ML Model if available and text is long enough to be ambiguous
    # Heuristics are better for short strings with definitive markers
    if ORTHOGRAPHY_MODEL:
        try:
            # If strong signals for both, let model decide (it sees n-gram frequency)
            # or if no obvious signals but we want a guess
            pred = ORTHOGRAPHY_MODEL.predict([text])[0]
            prob = ORTHOGRAPHY_MODEL.predict_proba([text]).max()
            
            # If the model is very confident, trust it
            if prob > 0.8:
                return pred
        except Exception:
            pass

    # 3. Fallback to heuristics
    if has_diaro and has_cunia:
        return "mixed"
    elif has_diaro:
        return "diaro"
    elif has_cunia:
        return "cunia"
    else:
        return "unknown"


def normalize_text(text: str, target: str = "cunia") -> str:
    """Normalize any Aromanian text to the specified standard.
    
    Args:
        text: Input text in any Aromanian orthography
        target: Target orthography ('cunia' or 'diaro')
        
    Returns:
        Normalized text in the target orthography
    """
    if target.lower() == "cunia":
        return to_cunia(text)
    elif target.lower() == "diaro":
        return to_diaro(text)
    else:
        raise ValueError(f"Unknown target orthography: {target}. Use 'cunia' or 'diaro'.")


def clean_text(text: str, lang: str = "rup") -> str:
    """Clean and normalize text for processing.
    
    Args:
        text: Input text
        lang: Language code ('rup' for Aromanian, 'ron' for Romanian)
        
    Returns:
        Cleaned text
    """
    text = re.sub(r"\s+", " ", text).strip()
    
    text = re.sub(r"(?<=\w)î(?=\w)", "â", text)
    
    if lang == "ron":
        text = text.replace("Ş", "Ș")
        text = text.replace("ş", "ș")
        text = text.replace("Ţ", "Ț")
        text = text.replace("ţ", "ț")
    else:
        text = to_cunia(text)
    
    text = text.replace("—", "-")
    text = text.replace("…", "...")
    text = text.replace("*", "")
    text = text.replace("<", "")
    text = text.replace(">", "")
    text = text.replace("„", '"')
    text = text.replace("”", '"')
    text = text.replace("“", '"')
    text = text.replace("‘", "'")
    text = text.replace("’", "'")
    
    return text


BOOK_TO_DIARO = [
    ("dz", "d̦"),
    ("Dz", "D̦"),
    ("l'", "ľ"),
    ("l'", "ľ"),
    ("L'", "Ľ"),
    ("L'", "Ľ"),
    ("ñ", "ń"),
    ("ş", "ș"),
    ("ţ", "ț"),
    ("Ş", "Ș"),
    ("Ţ", "Ț"),
    ("γ", "y"),
    ("Γ", "Y"),
]

BOOK_TO_CUNIA = [
    ("Ă", "ã"),
    ("Î", "ã"),
    ("î", "ã"),
    ("ă", "ã"),
    ("Â", "ã"),
    ("â", "ã"),
    ("l'", "lj"),
    ("l'", "lj"),
    ("L'I", "LJI"),
    ("L'I", "LJI"),
    ("L'", "Lj"),
    ("L'", "Lj"),
    ("ñ", "nj"),
    ("ş", "sh"),
    ("ţ", "ts"),
    ("ŞI", "SHI"),
    ("Ş", "Sh"),
    ("Ţ", "Ts"),
    ("ș", "sh"),
    ("ț", "ts"),
    ("Ș", "Sh"),
    ("Ț", "Ts"),
    ("γ", "y"),
    ("Γ", "Y"),
]


def apply_mapping(text: str, mapping: list) -> str:
    """Apply a character mapping to text.
    
    Args:
        text: Input text
        mapping: List of (from, to) tuples
        
    Returns:
        Text with mappings applied
    """
    for from_str, to_str in mapping:
        text = text.replace(from_str, to_str)
    return text


def book_to_diaro(text: str) -> str:
    """Convert from legacy 'book' orthography to DIARO standard."""
    return apply_mapping(text, BOOK_TO_DIARO)


def book_to_cunia(text: str) -> str:
    """Convert from legacy 'book' orthography to Cunia standard."""
    return apply_mapping(text, BOOK_TO_CUNIA)


if __name__ == "__main__":
    test_texts = [
        "Bunã dzua! Cum eshti?",
        "Bună dzua! Cum ești?",
        "Mini hiu armãn shi zburãscu armãneashti.",
    ]
    
    print("Testing orthography conversions:")
    print("=" * 50)
    
    # Force reload for main block if needed, though module level should handle it
    if not FREQ_AH:
         print("Note: Frequency maps not loaded in __main__ (normal if running script directly without installation)")

    for text in test_texts:
        print(f"\nOriginal: {text}")
        cunia = to_cunia(text)
        diaro = to_diaro(text)
        print(f"Cunia:    {cunia}")
        print(f"DIARO:    {diaro}")

