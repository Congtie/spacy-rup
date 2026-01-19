import spacy
from pathlib import Path
import spacy_rup

def verify_pos():
    model_path = Path("spacy_rup/resources/pos_model")
    if not model_path.exists():
        print(f"Error: Model not found at {model_path}")
        return

    print(f"Loading model from {model_path}...")
    try:
        nlp = spacy.load(model_path)
        print(f"Loaded pipeline components: {nlp.pipe_names}")
    except Exception as e:
        print(f"Failed to load model: {e}")
        return

    print("\nPOS Tagger Ready! Type a sentence to tag (or 'exit' to quit).")
    print("=" * 50)
    
    while True:
        try:
            text = input("\nText: ").strip()
        except EOFError:
            break
            
        if text.lower() in ("exit", "quit", "q"):
            break
            
        if not text:
            continue

        doc = nlp(text)
        print(f"\n{'Token':<15} {'Tag':<10} {'POS':<10}")
        print("-" * 35)
        for token in doc:
            print(f"{token.text:<15} {token.tag_:<10} {token.pos_:<10}")

if __name__ == "__main__":
    verify_pos()
