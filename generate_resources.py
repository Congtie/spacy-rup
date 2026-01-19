
import json
import re
from collections import defaultdict
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

if __name__ == "__main__":
    # Adjust paths as needed
    CORPUS_FILE = r"c:\Users\Taka\Desktop\spacy-rup\data\unsplit\corpus.rup_std"
    OUTPUT_DIR = r"c:\Users\Taka\Desktop\spacy-rup\spacy_rup\resources"
    
    generate_frequency_maps(CORPUS_FILE, OUTPUT_DIR)
