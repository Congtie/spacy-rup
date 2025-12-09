"""
Example sentences for Aromanian (rup) in both orthographies.
Used for testing the tokenizer and language model.

Orthographies:
- Cunia: ã/dz/lj/nj/sh/ts
- DIARO: ăâî/d̦/ľ/ń/ș/ț
"""

sentences = [
    # Basic sentences in Cunia orthography
    "Bunã dzua! Cum eshti?",
    "Mini hiu armãn shi zburãscu armãneashti.",
    "Noi bãnãm tru munts shi avem njilji di oi.",
    "Easti unã limbã multu musheatã.",
    "Tsintsi frats avea nãsh.",
    
    # Same in DIARO orthography
    "Bună dzua! Cum ești?",
    "Mini hiu armăn și zburăscu armănești.",
    "Noi bănăm tru munț și avem ńilji di oi.",
    "Easti ună limbă multu mușată.",
    "Țintsi frați avea năș.",
    
    # Longer text samples
    "Limba armãneascã easti unã limbã romanicã zburãtã tu Balcani.",
    "Armãnjlji bãneadzã tu Gãrtsie, Arbinishie, Makedonie shi Romãnie.",
    
    # With Greek-influenced vocabulary
    "Efharisto ti tutã! Adio shi cali oarã!",
    
    # Mixed with Romanian (common in texts)
    "Aestã easti limba a noastrã armãneascã.",
    
    # Questions
    "Tsi fats? Iu ti duts?",
    "Cãtã anj ai? Di iu eshti?",
    
    # Negation
    "Nu shtiu tsi s-dzãcã.",
    "N-am vidzutã vãrãoarã ahtari lucru.",
    
    # Complex sentences
    "Cãndu eara njic, bãneam tru sat shi earamu multu harauã.",
    "Tra s-aibã suctsesã, lipseashti s-lucreadz multu.",
]


# Tokenization test cases - expected token lists
tokenization_tests = [
    (
        "Bunã dzua!",
        ["Bunã", "dzua", "!"]
    ),
    (
        "Mini s-hiu armãn.",
        ["Mini", "s-", "hiu", "armãn", "."]
    ),
    (
        "Dzã-nj tsi vrets.",
        ["Dzã", "-", "nj", "tsi", "vrets", "."]
    ),
    (
        "L-om ahtari lucru.",
        ["L-", "om", "ahtari", "lucru", "."]
    ),
    (
        "Etc. shi ashi.",
        ["Etc.", "shi", "ashi", "."]
    ),
]
