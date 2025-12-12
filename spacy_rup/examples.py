"""
Example sentences for Aromanian (rup) in both orthographies.
Used for testing the tokenizer and language model.

Orthographies:
- Cunia: ã/dz/lj/nj/sh/ts
- DIARO: ăâî/d̦/ľ/ń/ș/ț
"""

sentences = [
    "Bunã dzua! Cum eshti?",
    "Mini hiu armãn shi zburãscu armãneashti.",
    "Noi bãnãm tru munts shi avem njilji di oi.",
    "Easti unã limbã multu musheatã.",
    "Tsintsi frats avea nãsh.",
    
    "Bună dzua! Cum ești?",
    "Mini hiu armăn și zburăscu armănești.",
    "Noi bănăm tru munț și avem ńilji di oi.",
    "Easti ună limbă multu mușată.",
    "Țintsi frați avea năș.",
    
    "Limba armãneascã easti unã limbã romanicã zburãtã tu Balcani.",
    "Armãnjlji bãneadzã tu Gãrtsie, Arbinishie, Makedonie shi Romãnie.",
    
    "Efharisto ti tutã! Adio shi cali oarã!",
    
    "Aestã easti limba a noastrã armãneascã.",
    
    "Tsi fats? Iu ti duts?",
    "Cãtã anj ai? Di iu eshti?",
    
    "Nu shtiu tsi s-dzãcã.",
    "N-am vidzutã vãrãoarã ahtari lucru.",
    
    "Cãndu eara njic, bãneam tru sat shi earamu multu harauã.",
    "Tra s-aibã suctsesã, lipseashti s-lucreadz multu.",
]


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
