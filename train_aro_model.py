
import os
import pickle
import glob
from pathlib import Path
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

def load_data(data_dir):
    """
    Load data from:
    1. data/basma_cunia.txt + data/unsplit/corpus.rup_cun -> Label: 'cunia'
    2. data/basma_diaro.txt + data/unsplit/corpus.rup_std -> Label: 'diaro'
    
    Explicitly ignores .ro files.
    """
    data = []
    labels = []
    
    # Define file mappings
    sources = [
        {"path": "data/basma_cunia.txt", "label": "cunia"},
        {"path": "data/unsplit/corpus.rup_cun", "label": "cunia"},
        {"path": "data/basma_diaro.txt", "label": "diaro"},
        {"path": "data/unsplit/corpus.rup_std", "label": "diaro"},
    ]
    
    print("Loading data...")
    for source in sources:
        filepath = Path(data_dir) / source["path"]
        # Handle cases where path might be relative to script or absolute
        if not filepath.exists():
            # Try looking in current dir if script run from root
            filepath = Path(source["path"])
            
        if filepath.exists():
            print(f"  Reading: {filepath}")
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    # Basic cleaning
                    lines = [line.strip() for line in lines if line.strip()]
                    
                    data.extend(lines)
                    labels.extend([source["label"]] * len(lines))
                    print(f"    -> Added {len(lines)} samples.")
            except Exception as e:
                print(f"    Error reading file: {e}")
        else:
            print(f"  Warning: File not found: {filepath}")

    return data, labels

def train_model():
    base_dir = Path(__file__).parent
    
    # Load data
    texts, labels = load_data(base_dir)
    
    if not texts:
        print("Error: No data loaded. Aborting training.")
        return

    print(f"Total samples: {len(texts)}")
    print(f"Distribution: Cunia={labels.count('cunia')}, Diaro={labels.count('diaro')}")
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)
    
    # Pipeline: Character n-grams are best for orthography detection
    # 'sh', 'ts', 'ã' vs 'ș', 'ț', 'ă' are character level differences.
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(analyzer='char', ngram_range=(1, 3), min_df=2)),
        ('clf', MultinomialNB()),
    ])
    
    print("Training model...")
    pipeline.fit(X_train, y_train)
    
    # Evaluate
    print("Evaluating...")
    preds = pipeline.predict(X_test)
    print(classification_report(y_test, preds))
    print(f"Accuracy: {accuracy_score(y_test, preds):.4f}")
    
    # Manual Sanity Check
    test_phrases = [
        "Bunã dzua, cum s-dzuce?", # Cunia
        "Bună dzua, cum s-dzuce?", # Diaro
        "si cum dipuse", # Likely Diaro (si vs shi), though 'dipuse' might be ambiguous
        "shi cum dipuse", # Likely Cunia (shi)
    ]
    print("\nSanity Check:")
    for phrase in test_phrases:
        pred = pipeline.predict([phrase])[0]
        prob = pipeline.predict_proba([phrase]).max()
        print(f"  '{phrase}' -> {pred} ({prob:.2f})")

    # Save
    output_dir = base_dir / "spacy_rup" / "resources"
    output_dir.mkdir(parents=True, exist_ok=True)
    model_path = output_dir / "orthography_model.pkl"
    
    with open(model_path, 'wb') as f:
        pickle.dump(pipeline, f)
        
    print(f"\nModel saved to {model_path}")

if __name__ == "__main__":
    train_model()
