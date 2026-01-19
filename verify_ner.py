import spacy
import spacy_rup  # Register the Aromanian language
from pathlib import Path

def verify_ner():
    model_path = Path("spacy_rup/resources/ner_model")
    print(f"Loading model from {model_path}...")
    nlp = spacy.load(model_path)
    
    # Test sentences - exact matches from training corpus with known entities
    test_sentences = [
        # From training: has ORGANIZATION entity "AL NASTRADIN-HOGEA"
        "DI AL NASTRADIN-HOGEA",
        # From training: has PRODUCT entity "tavă"
        "Horiatlu a nostru și-avea adusă deacasă, tru ună tavă, ună găl'ină umplută cu făstăț, stafidz, orez și alte.",
        # From training: has GPE entity "Moreee"
        "- Moreee, ți săndze lai au ș-γifțîl'i aești - dzăse un aschirlî!",
        # From training: has PERSON entity
        "Așe s-mindui γiftul Thimñiul cu treil'i-a lui ficiori: Cotta, Cola și Albul.",
        # From training: has NUMERIC_VALUE
        "Eară ună oară trei călători.",
    ]
    
    print("\nTesting NER:\n")
    found_count = 0
    for sent in test_sentences:
        doc = nlp(sent)
        print(f"Propoz: {sent}")
        if doc.ents:
            for ent in doc.ents:
                print(f"  ✓ Entity: '{ent.text}' ({ent.label_})")
                found_count += 1
        else:
            print("  ✗ No entities found.")
        print()
    
    print(f"Total entities found: {found_count}")

if __name__ == "__main__":
    verify_ner()
