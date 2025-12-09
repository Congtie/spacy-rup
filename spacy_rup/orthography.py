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
from pathlib import Path


# Mapping tables for orthographic conversion
# Cunia to DIARO consonant mapping
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

# DIARO to Cunia consonant mapping (reverse)
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
    "l'": "lj",  # different apostrophe
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

# Central vowel normalization to Cunia (ã)
VOWELS_TO_CUNIA = {
    "ă": "ã",
    "Ă": "Ã",
    "â": "ã",
    "Â": "Ã",
    "î": "ã",
    "Î": "Ã",
    "ӑ": "ã",  # Cyrillic-looking variant
    "Ӑ": "Ã",
    "ǎ": "ã",
    "Ǎ": "Ã",
}

# Other character normalizations
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
    
    # Use n-gram data if available
    if fah and fuh:
        # Get 4-character context around the position
        start = max(0, position - 2)
        end = min(len(word), position + 3)
        context = word[start:end].lower()
        
        cnt_ah = fah.get(context, 0)  # Count favoring â
        cnt_uh = fuh.get(context, 0)  # Count favoring ă
        
        if cnt_ah > cnt_uh:
            return "â"
        else:
            return "ă"
    
    # Default heuristic: use â in the middle, ă otherwise
    # This is a simplification; real conversion needs dictionary lookup
    return "ă"


def to_diaro(text: str, fah: Optional[dict] = None, fuh: Optional[dict] = None) -> str:
    """Convert text to DIARO orthography (ăâî/d̦/ľ/ń/ș/ț).
    
    Args:
        text: Input text (ideally already in Cunia for best results)
        fah: Optional n-gram frequency dict for â resolution
        fuh: Optional n-gram frequency dict for ă resolution
        
    Returns:
        Text converted to DIARO standard
    """
    # First ensure we're in Cunia as intermediate
    text = to_cunia(text)
    
    # Process word by word for vowel resolution
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
    
    # Convert each word
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
            # Convert consonants to DIARO
            converted = convert_consonants_to_diaro(converted)
            result.append(converted)
        else:
            result.append(token)
    
    return "".join(result)


def cunia_to_diaro(text: str) -> str:
    """Convenience function: Convert Cunia to DIARO.
    
    Note: Without n-gram frequency data, this uses heuristics for vowel resolution.
    For best results, load the frequency dictionaries from resources.
    """
    return to_diaro(text)


def diaro_to_cunia(text: str) -> str:
    """Convenience function: Convert DIARO to Cunia."""
    return to_cunia(text)


def detect_orthography(text: str) -> str:
    """Detect which orthographic standard a text uses.
    
    Args:
        text: Input Aromanian text
        
    Returns:
        'cunia', 'diaro', 'mixed', or 'unknown'
    """
    # DIARO-specific characters: ș, ț, ă, â, î, ľ, ń, d̦
    diaro_chars = set("șțăâîľńd̦ȘȚĂÂÎĽŃ")
    # Cunia-specific patterns: sh, ts, lj, nj, dz, ã
    cunia_patterns = ["sh", "ts", "lj", "nj", "dz"]
    cunia_chars = set("ã")
    
    has_diaro = any(c in diaro_chars for c in text)
    has_cunia_char = any(c in cunia_chars for c in text)
    has_cunia_pattern = any(p in text.lower() for p in cunia_patterns)
    has_cunia = has_cunia_char or has_cunia_pattern
    
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
    # Consecutive spaces
    text = re.sub(r"\s+", " ", text).strip()
    
    # Old Romanian î in the middle of the word (for mixed texts)
    text = re.sub(r"(?<=\w)î(?=\w)", "â", text)
    
    if lang == "ron":
        # Romanian: normalize cedilla variants
        text = text.replace("Ş", "Ș")
        text = text.replace("ş", "ș")
        text = text.replace("Ţ", "Ț")
        text = text.replace("ţ", "ț")
    else:
        # Aromanian: convert to Cunia as default
        text = to_cunia(text)
    
    # Common punctuation normalization
    text = text.replace("—", "-")
    text = text.replace("…", "...")
    text = text.replace("*", "")
    text = text.replace("<", "")
    text = text.replace(">", "")
    text = text.replace("„", '"')
    text = text.replace(""", '"')
    text = text.replace(""", '"')
    text = text.replace("'", "'")
    text = text.replace("'", "'")
    
    return text


# Book to DIARO mapping (from senisioi/aromanian)
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

# Book to Cunia mapping
BOOK_TO_CUNIA = [
    ("Ă", "Ã"),
    ("Î", "Ã"),
    ("î", "ã"),
    ("ă", "ã"),
    ("Â", "Ã"),
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
    # Test the conversions
    test_texts = [
        "Bunã dzua! Cum eshti?",  # Cunia
        "Bună dzua! Cum ești?",    # DIARO (partial)
        "Mini hiu armãn shi zburãscu armãneashti.",  # Cunia
    ]
    
    print("Testing orthography conversions:")
    print("=" * 50)
    
    for text in test_texts:
        print(f"\nOriginal: {text}")
        cunia = to_cunia(text)
        diaro = to_diaro(text)
        print(f"Cunia:    {cunia}")
        print(f"DIARO:    {diaro}")
