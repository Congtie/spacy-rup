import spacy
from pathlib import Path
import spacy_rup

def verify_pos_auto():
    model_path = Path("spacy_rup/resources/pos_model")
    if not model_path.exists():
        print(f"Error: Model not found at {model_path}")
        return

    print(f"Loading model from {model_path}...")
    try:
        nlp = spacy.load(model_path)
    except Exception as e:
        print(f"Failed to load model: {e}")
        return

    test_sentences = [
        "Dă-nji ună măr!",            # Give me an apple (Imperative + Clitic)
        "Am dauă căsuri.",            # I have two houses (Number)
        "Nu s-poati s-fugă.",         # It is not possible to run (Modal)
        "Câți oaminji suntu?",        # How many people are there? (Interrogative)
        "Mine nu escu a tău.",        # I am not yours (Pronouns)
    ]

    print("\nTest Results:")
    print("-" * 50)
    for sent in test_sentences:
        doc = nlp(sent)
        print(f"\nText: {sent}")
        print(f"{'Token':<15} {'Tag':<10} {'POS':<10}")
        print("-" * 35)
        for token in doc:
            print(f"{token.text:<15} {token.tag_:<10} {token.pos_:<10}")

if __name__ == "__main__":
    verify_pos_auto()
