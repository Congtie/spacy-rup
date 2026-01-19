
import json
import re
from collections import defaultdict
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from pathlib import Path

def generate_frequency_maps(corpus_path, output_dir):
    """
    Generate frequency maps for 'â' (ah) and 'ă' (uh) contexts from a DIARO corpus.
    """
    print(f"Reading corpus from: {corpus_path}")
    
    try:
        with open(corpus_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: Corpus file not found at {corpus_path}")
        return

    # Normalize spaces
    words = re.findall(r'\b\w+\b', text.lower())
    
    fah = defaultdict(int)  # Frequency for 'â'
    fuh = defaultdict(int)  # Frequency for 'ă'
    
    count_ah = 0
    count_uh = 0
    
    print(f"Processing {len(words)} words...")
    
    for word in words:
        # Skip words that don't contain target chars
        if 'â' not in word and 'ă' not in word:
            continue
            
        for i, char in enumerate(word):
            if char in ['â', 'ă']:
                # Extract context: 2 chars before, 2 chars after + current
                # Store as 5-char window relative to the target position
                start = max(0, i - 2)
                end = min(len(word), i + 3)
                context = word[start:end]
                
                # We need to store the context with a placeholder to match potentially different target vowels
                # But typically we just want to know: "in context X, is it usually â or ă?"
                # So we store the exact context string found in valid DIARO text.
                
                # Actually, the logic in orthography.py checks:
                # context = word[start:end]
                # fah.get(context) vs fuh.get(context)
                # So we just store the exact string as it appears in valid text.
                
                if char == 'â':
                    fah[context] += 1
                    count_ah += 1
                elif char == 'ă':
                    fuh[context] += 1
                    count_uh += 1

    print(f"Generated stats: 'â' contexts: {len(fah)}, 'ă' contexts: {len(fuh)}")
    print(f"Total occurrences: 'â': {count_ah}, 'ă': {count_uh}")

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Save to JSON
    with open(output_path / 'freq_ah.json', 'w', encoding='utf-8') as f:
        json.dump(fah, f, ensure_ascii=False, indent=2)
        
    with open(output_path / 'freq_uh.json', 'w', encoding='utf-8') as f:
        json.dump(fuh, f, ensure_ascii=False, indent=2)
        
    print(f"Maps saved to {output_dir}")

def train_model(corpus_std, corpus_cun, output_dir):
    """
    Train a simple Naive Bayes model to distinguish between Standard (DIARO) and Cunia.
    """
    print("Training Orthography Identification Model...")
    
    texts = []
    labels = []
    
    # Load DIARO data
    if Path(corpus_std).exists():
        with open(corpus_std, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    texts.append(line.strip())
                    labels.append("diaro")
    else:
        print(f"Warning: DIARO corpus not found at {corpus_std}")

    # Load Cunia data
    if Path(corpus_cun).exists():
        with open(corpus_cun, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    texts.append(line.strip())
                    labels.append("cunia")
    else:
        print(f"Warning: Cunia corpus not found at {corpus_cun}")
        
    if not texts:
        print("No training data found for model!")
        return

    # Train Pipeline
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(analyzer='char', ngram_range=(2, 4))),
        ('clf', MultinomialNB()),
    ])
    
    pipeline.fit(texts, labels)
    
    # Save
    output_path = Path(output_dir) / "orthography_model.pkl"
    with open(output_path, "wb") as f:
        pickle.dump(pipeline, f)
        
    print(f"Model saved to {output_path}")

if __name__ == "__main__":
    # Adjust paths as needed
    # Adjust paths as needed
    base_dir = Path(__file__).parent
    CORPUS_FILE = base_dir / "data" / "unsplit" / "corpus.rup_std"
    CORPUS_CUN = base_dir / "data" / "unsplit" / "corpus.rup_cun"
    OUTPUT_DIR = base_dir / "spacy_rup" / "resources"
    
    generate_frequency_maps(CORPUS_FILE, OUTPUT_DIR)
    train_model(CORPUS_FILE, CORPUS_CUN, OUTPUT_DIR)
