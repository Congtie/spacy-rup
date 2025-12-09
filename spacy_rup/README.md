# spaCy Language Support for Aromanian (rup)

## Overview

This folder contains the language data for Aromanian (Macedo-Romanian), an endangered Eastern Romance language spoken in the Balkans.

**ISO 639-3 code:** `rup`

**Language family:** Romance > Eastern Romance

**Native name:** armãneashti, armãnã, rrãmãneshti

## Writing Standards

Aromanian has multiple orthographic standards, which creates challenges for NLP:

### 1. DIARO Standard (Caragiu-Marioțeanu)
- Linguistically motivated, used in academic contexts
- Central vowels: **ă**, **â**, **î**
- Special consonants: **d̦** (dz), **ľ** (palatal l), **ń** (palatal n), **ș**, **ț**
- Example: *Bună dzua! Cum ești?*

### 2. Cunia Standard (Tiberiu Cunia)
- Practical for digital typing
- Unified central vowel: **ã**
- Digraphs: **dz**, **lj**, **nj**, **sh**, **ts**
- Example: *Bunã dzua! Cum eshti?*

### 3. Other Variants
- **Wikipedia style:** Uses apostrophe (l' instead of ľ)
- **Greek-based:** Uses Greek letters for some sounds (θ, δ, γ)
- **Legacy book encodings:** Various conventions from printed sources

## File Structure

```
spacy_rup/
├── __init__.py           # Language class definition
├── stop_words.py         # Common function words
├── tokenizer_exceptions.py # Abbreviations, contractions
├── punctuation.py        # Prefix/suffix/infix rules
├── lex_attrs.py          # Lexical attributes (numbers, etc.)
├── orthography.py        # Conversion between standards
├── examples.py           # Test sentences
└── README.md             # This file
```

## Installation

To add this language to spaCy:

### Option 1: Local Development
1. Clone spaCy repository:
   ```bash
   git clone https://github.com/explosion/spaCy.git
   cd spaCy
   ```

2. Copy this folder to `spacy/lang/rup/`:
   ```bash
   cp -r /path/to/spacy_rup spacy/lang/rup
   ```

3. Register the language in `spacy/lang/__init__.py`:
   ```python
   from .rup import Aromanian
   ```

4. Install spaCy in development mode:
   ```bash
   pip install -e .
   ```

### Option 2: As External Package
```python
from spacy.lang.rup import Aromanian
nlp = Aromanian()
```

## Usage

```python
from spacy.lang.rup import Aromanian

# Create language instance
nlp = Aromanian()

# Process text (Cunia orthography)
doc = nlp("Bunã dzua! Mini hiu armãn.")

for token in doc:
    print(token.text, token.is_stop, token.like_num)
```

### With Orthography Conversion

```python
from spacy_rup.orthography import to_cunia, to_diaro

# Normalize input before processing
text_diaro = "Bună dzua! Cum ești?"
text_cunia = to_cunia(text_diaro)  # "Bunã dzua! Cum eshti?"

doc = nlp(text_cunia)
```

## Linguistic Notes

### Phonology
- Central vowels: /ə/ (ă/ã), /ɨ/ (î/â/ã)
- Palatal consonants: /ʎ/ (ľ/lj), /ɲ/ (ń/nj)
- Affricates: /dz/ (d̦/dz), /ts/ (ț/ts)

### Grammar
- Similar to Romanian but with archaic features
- Definite article suffixed to nouns
- Rich clitic system

### Vocabulary
- Significant Greek influence
- Slavic loanwords from contact languages
- Retains Latin features lost in Romanian

## Resources

- **Dataset:** https://github.com/senisioi/aromanian
- **Translator:** https://arotranslate.com
- **Conversion scripts:** https://github.com/arotranslate/AroTranslate

## References

1. Petrariu, I., & Nisioi, S. (2024). A Multilingual Parallel Corpus for Aromanian. *LREC-COLING 2024*.

2. Jerpelea, A.-I., Radoi, A., & Nisioi, S. (2025). Dialectal and Low Resource Machine Translation for Aromanian. *COLING 2025*.

3. Caragiu-Marioțeanu, M. (1997). *Dicționar aromân (macedo-vlah): DIARO*.

4. Cunia, T. (1997). *On the Standardization of the Aromanian System of Writing*.

## Contributing

Contributions are welcome! Areas that need work:
- Expanding stop words list
- Adding more tokenizer exceptions
- Improving n-gram data for vowel resolution
- Adding lemmatization rules
- Creating training data for POS tagging

## License

Same as spaCy (MIT License)
