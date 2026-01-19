# spaCy Language Support for Aromanian (rup)

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![spaCy 3.x](https://img.shields.io/badge/spaCy-3.x-green.svg)](https://spacy.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A complete spaCy language module for **Aromanian** (Macedo-Romanian), an endangered Eastern Romance language spoken in the Balkans.

## Language Code

- **ISO 639-3:** `rup` (Aromanian / Macedo-Romanian / Armaneashti)
- **Speakers:** ~250,000 (Greece, Albania, North Macedonia, Romania, Bulgaria, Serbia)

## Features

| Component | Status | Description |
|-----------|--------|-------------|
| Tokenizer | :white_check_mark: | Rules for Aromanian clitics (s-, sh-, n-, lj-, etc.) |
| Stop Words | :white_check_mark: | 163+ function words |
| Lex Attrs | :white_check_mark: | Number detection (un, doi, trei, dzatsi...) |
| Orthography | :white_check_mark: | Conversion between Cunia and DIARO standards |
| **Lemmatizer** | :white_check_mark: | Lookup tables + suffix rules for verbs, nouns, adjectives |
| POS Tagger | :white_check_mark: | Trained via `train_pos_model.py` |
| NER | :white_check_mark: | Trained via `train_ner_model.py` |

## Installation

```bash
# Clone the repository
git clone https://github.com/Congtie/spacy-rup.git
cd spacy-rup

# Install in development mode
pip install -e .
```

## Quick Start

```python
import spacy

# Create a blank Aromanian pipeline
nlp = spacy.blank('rup')

# Add the lemmatizer
nlp.add_pipe('aromanian_lemmatizer')

# Process text
doc = nlp("Ficiorlu featse un lucru multu bun.")
for token in doc:
    print(f"{token.text:15} -> {token.lemma_}")
```

Output:
```
Ficiorlu        -> ficior
featse          -> fac
un              -> un
lucru           -> lucru
multu           -> multu
bun             -> bun
.               -> .
```

## Lemmatizer

The lemmatizer handles Aromanian morphology through:

### Verb Lemmatization
Supports irregular verbs with full conjugation lookup:

| Verb | Forms | Lemma |
|------|-------|-------|
| a hi (to be) | hiu, eshti, easti, eara, fu, fura | `hiu` |
| a avea (to have) | am, ai, are, avea, aveam, avura | `am` |
| a fac (to do) | fac, fatse, featse, featsira | `fac` |
| a dzac (to say) | dzac, dzatse, dzatsea | `dzac` |
| a vrea (to want) | vrea, va, vor, vrura | `vrea` |
| a vedu (to see) | vedu, vedz, vidzu, vidzura | `vedu` |
| a yinu (to come) | yin, yine, yinea, vinje | `yinu` |
| a ljau (to take) | ljau, ljea, lo, loara | `ljau` |

### Noun Lemmatization
Removes definite articles:

| With Article | Lemma | Meaning |
|--------------|-------|---------|
| ficiorlu | ficior | boy |
| amiralu | amira | emperor |
| vulpea | vulpe | fox |
| calea | cale | way |
| ocljilji | oclji | eyes |

### Example

```python
import spacy

nlp = spacy.blank('rup')
nlp.add_pipe('aromanian_lemmatizer')

# Verb lemmatization
doc = nlp("Eara una oara un om shi avea trei ficiori")
changes = [(t.text, t.lemma_) for t in doc if t.text.lower() != t.lemma_]
print(changes)
# [('Eara', 'hiu'), ('avea', 'am')]
```

## Orthographic Standards

Aromanian has multiple writing systems. This module supports both:

| Standard | Central Vowel | Special Consonants | Example |
|----------|--------------|-------------------|---------|
| **DIARO** | ă, â, î | d̦, ľ, ń, ș, ț | Bună dzua! |
| **Cunia** | ã | dz, lj, nj, sh, ts | Bunã dzua! |

### Conversion

```python
from spacy_rup.orthography import to_cunia, to_diaro, detect_orthography

# Detect standard
detect_orthography("Shi una vulpe")  # "cunia"

# Convert between standards
text_diaro = "Și una vulpe"
text_cunia = to_cunia(text_diaro)  # "Shi una vulpe"
```


## Training

You can train your own POS Tagger and Named Entity Recognizer using the provided scripts.

### POS Tagger Training

1. Ensure training data is at `data/train.rup.conll`
2. Run the training script:
   ```bash
   python train_pos_model.py
   ```
   The model will be saved to `spacy_rup/resources/pos_model`.

### NER Training

1. Ensure training data is at `data/train.rup.ner.json`
2. Run the training script:
   ```bash
   python train_ner_model.py
   ```
   The model will be saved to `spacy_rup/resources/ner_model`.

## Project Structure

```
spacy-rup/
├── spacy_rup/
│   ├── __init__.py          # Language class (Aromanian)
│   ├── stop_words.py        # 163+ stop words
│   ├── tokenizer_exceptions.py  # Clitic contractions
│   ├── punctuation.py       # Prefix/suffix rules
│   ├── lex_attrs.py         # Number words
│   ├── orthography.py       # Cunia <-> DIARO conversion
│   ├── lemmatizer.py        # Lookup tables and rules
│   └── lemma_component.py   # spaCy pipeline component
├── setup.py
└── README.md
```

## Data Sources

- **Corpus:** [senisioi/aromanian](https://github.com/senisioi/aromanian) - ~2100 parallel sentences (Aromanian Tales)
- **Conversion Scripts:** [AroTranslate](https://github.com/arotranslate/AroTranslate)

## Contributing

Contributions welcome! Areas that need help:

1. **More verb forms** - Add conjugations to `lemmatizer.py`
2. **POS tagger training** - Annotated data needed
3. **Named Entity Recognition** - Location/person names
4. **Dialect variations** - Farsherot, Gramustean, etc.
5. **Testing** - More test cases

## License

MIT License

## References

- [Aromanian on Wikipedia](https://en.wikipedia.org/wiki/Aromanian_language)
- [spaCy Language Data](https://spacy.io/usage/adding-languages)
- [ISO 639-3 rup](https://iso639-3.sil.org/code/rup)
- [Aromanian Grammar](https://aromanian.org/)

---

*Buna dzua! S-hiba ghine!* (Good day! May it be well!)
