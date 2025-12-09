# spaCy Language Support for Aromanian (rup)

This repository contains the language module for Aromanian (Macedo-Romanian) in spaCy.

## Language Code

- **ISO 639-3:** `rup` (Aromanian / Macedo-Romanian)

## Features

| Component | Status | Description |
|-----------|--------|-------------|
| Tokenizer | ✅ | Rules for Aromanian clitics (s-, sh-, n-, etc.) |
| Stop Words | ✅ | 163+ function words |
| Lex Attrs | ✅ | Number detection (un, doi, trei, dzatsi...) |
| Orthography | ✅ | Conversion between Cunia and DIARO standards |
| POS Tagger | ❌ | Requires training data |
| NER | ❌ | Requires training data |
| Lemmatizer | ❌ | Requires dictionary |

## Orthographic Standards

Aromanian has multiple writing systems:

| Standard | Central Vowel | Special Consonants | Example |
|----------|--------------|-------------------|---------|
| **DIARO** (Caragiu-Marioțeanu) | ă, â, î | d̦, ľ, ń, ș, ț | Bună dzua! |
| **Cunia** (Tiberiu Cunia) | ã | dz, lj, nj, sh, ts | Bunã dzua! |

This module handles both standards and can convert between them.

## Installation

### Option 1: Copy to spaCy installation

```bash
# Find your spaCy installation
python -c "import spacy; print(spacy.__file__)"

# Copy the module
cp -r spacy_rup /path/to/site-packages/spacy/lang/rup
```

### Option 2: Use install script

```bash
python install_rup.py
```

## Usage

```python
import spacy

# Create a blank Aromanian pipeline
nlp = spacy.blank('rup')

# Or import the language class directly
from spacy.lang.rup import Aromanian
nlp = Aromanian()

# Tokenize text
doc = nlp("Bunã dzua! S-hibã ghine.")
for token in doc:
    print(f"{token.text:15} stop={token.is_stop}")
```

Output:
```
Bunã            stop=False
dzua            stop=False
!               stop=False
S-              stop=False
hibã            stop=False
ghine           stop=True
.               stop=False
```

## Orthography Conversion

```python
from spacy_rup.orthography import to_cunia, to_diaro, detect_orthography

# Convert between standards
text_diaro = "Și ună vulpe"
text_cunia = to_cunia(text_diaro)  # "Shi unã vulpe"

# Detect which standard is used
detect_orthography("Shi unã vulpe")  # "cunia"
detect_orthography("Și ună vulpe")   # "diaro"
```

## Testing

```bash
# Run local tests (no spaCy installation required)
python test_local.py

# After installation, run full tests
python -c "from spacy.lang.rup import Aromanian; nlp = Aromanian(); print(nlp('Test').text)"
```

## Data Sources

- **Corpus:** [senisioi/aromanian](https://github.com/senisioi/aromanian) - ~2000 parallel sentences
- **Conversion Scripts:** [AroTranslate](https://github.com/arotranslate/AroTranslate)

## Contributing

Contributions are welcome! Areas that need improvement:

1. More tokenizer exceptions for complex clitics
2. POS tagging training data
3. Named Entity Recognition data
4. Lemmatization rules or dictionary
5. Improved orthography conversion

## License

MIT License

## References

- [Aromanian on Wikipedia](https://en.wikipedia.org/wiki/Aromanian_language)
- [spaCy Language Data](https://spacy.io/usage/adding-languages)
- [ISO 639-3 rup](https://iso639-3.sil.org/code/rup)
