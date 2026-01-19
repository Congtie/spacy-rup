import spacy
from spacy.tokens import Doc, Span
from pathlib import Path
from spacy_rup import Aromanian
import difflib
import json

def project_ner_tags():
    # Load Romanian model for tagging source text
    try:
        nlp_ro = spacy.load("ro_core_news_sm")
    except OSError:
        print("Error: ro_core_news_sm not found. Please install it with: python -m spacy download ro_core_news_sm")
        return

    # Initialize Aromanian nlp for tokenization
    # Disable other pipes for speed/purity
    nlp_rup = Aromanian()

    data_dir = Path("data")
    ro_path = data_dir / "Tales.train.ro"
    rup_path = data_dir / "Tales.train.rup"
    output_path = data_dir / "train.rup.ner.json" # Use JSON format for spans

    if not ro_path.exists() or not rup_path.exists():
        print(f"Error: Corpus files not found in {data_dir}")
        return

    print(f"Reading from {ro_path} and {rup_path}...")
    
    with open(ro_path, "r", encoding="utf-8") as f:
        ro_lines = f.readlines()
    with open(rup_path, "r", encoding="utf-8") as f:
        rup_lines = f.readlines()

    assert len(ro_lines) == len(rup_lines), "Corpus files must have same number of lines"

    projected_sentences = 0
    total_sentences = len(ro_lines)
    
    training_data = []


    for i, (ro_line, rup_line) in enumerate(zip(ro_lines, rup_lines)):
        ro_line = ro_line.strip()
        rup_line = rup_line.strip()
        
        if not ro_line or not rup_line:
            continue

        # Process Romanian to get entities
        doc_ro = nlp_ro(ro_line)
        
        # Tokenize Aromanian
        doc_rup = nlp_rup(rup_line)
        
        ro_tokens = [t.text for t in doc_ro]
        rup_tokens = [t.text for t in doc_rup]

        # 1. Base Alignment using SequenceMatcher
        matcher = difflib.SequenceMatcher(None, 
            [t.lower() for t in ro_tokens], 
            [t.lower() for t in rup_tokens]
        )
        
        # Map ro_idx -> rup_idx for high confidence matches
        ro_to_rup_map = {}
        opcodes = matcher.get_opcodes()
        
        for tag, i1, i2, j1, j2 in opcodes:
            if tag == 'equal':
                for k in range(i2-i1):
                    ro_to_rup_map[i1 + k] = j1 + k
            elif tag == 'replace':
                # Heuristic: if lengths are close, assume linear mapping for simple cases
                # But better: Just leave unmapped and let the fuzzy search handle it
                # UNLESS it's a very obvious 1-to-1 cognate
                if (i2 - i1) == (j2 - j1):
                     for k in range(i2 - i1):
                        ro_word = ro_tokens[i1 + k]
                        rup_word = rup_tokens[j1 + k]
                        sim = difflib.SequenceMatcher(None, ro_word.lower(), rup_word.lower()).ratio()
                        if sim > 0.6: # Lower threshold essentially for "replace" blocks which imply some difference
                             ro_to_rup_map[i1 + k] = j1 + k

        # 2. Project Entities
        rup_ents = []
        
        for ent in doc_ro.ents:
            # Try 1: Direct Mapping
            ro_indices = list(range(ent.start, ent.end))
            mapped_rup_indices = [ro_to_rup_map[idx] for idx in ro_indices if idx in ro_to_rup_map]
            
            # If we have a perfect mapping
            if len(mapped_rup_indices) == len(ro_indices):
                 # Check contiguous
                 is_contiguous = all(mapped_rup_indices[j] == mapped_rup_indices[j-1] + 1 for j in range(1, len(mapped_rup_indices)))
                 if is_contiguous:
                     start_char = doc_rup[mapped_rup_indices[0]].idx
                     last_token = doc_rup[mapped_rup_indices[-1]]
                     end_char = last_token.idx + len(last_token)
                     rup_ents.append((start_char, end_char, ent.label_))
                     continue

            # Try 2: Fuzzy Search in Window
            # Determine search window in RUP based on surrounding mapped tokens
            # Find closest mapped token to the left
            left_bound = 0
            for idx in range(ent.start - 1, -1, -1):
                if idx in ro_to_rup_map:
                    left_bound = ro_to_rup_map[idx]
                    break
            
            # Find closest mapped token to the right
            right_bound = len(rup_tokens)
            for idx in range(ent.end, len(ro_tokens)):
                if idx in ro_to_rup_map:
                    right_bound = ro_to_rup_map[idx] + 1 # +1 to include
                    break
            
            # Extract RUP window
            # Relax window slightly
            window_start = max(0, left_bound)
            window_end = min(len(rup_tokens), right_bound + 2) # +2 slack
            
            window_tokens = doc_rup[window_start:window_end]
            if not window_tokens:
                continue
                
            # Construct Entity String
            ent_text = ent.text.lower()
            
            # Scan window for best n-gram match
            # We look for a sequence of tokens in window that matches ent_text
            best_match_score = 0.0
            best_match_span = None
            
            target_len = len(ro_indices) # Expected number of tokens (approx)
            
            # Try spans of length target_len +/- 1
            for l in range(max(1, target_len - 1), min(len(window_tokens), target_len + 2) + 1):
                for k in range(len(window_tokens) - l + 1):
                    cand_span = window_tokens[k : k+l]
                    cand_text = cand_span.text.lower()
                    
                    # Compute similarity
                    sim = difflib.SequenceMatcher(None, ent_text, cand_text).ratio()
                    
                    if sim > best_match_score:
                        best_match_score = sim
                        best_match_span = cand_span
            
            # Threshold for fuzzy match
            if best_match_score > 0.8: # High confidence
                rup_ents.append((best_match_span.start_char, best_match_span.end_char, ent.label_))
        
        # Deduplicate entities (in case of overlap, though unlikely with this logic)
        # Sort by start
        rup_ents.sort(key=lambda x: x[0])
        # Simple overlap removal: if start < prev_end, skip
        final_ents = []
        if rup_ents:
            curr = rup_ents[0]
            final_ents.append(curr)
            for next_ent in rup_ents[1:]:
                if next_ent[0] >= curr[1]:
                    final_ents.append(next_ent)
                    curr = next_ent
        
        if final_ents:
            training_data.append((rup_line, {"entities": final_ents}))
            projected_sentences += 1

    print(f"Done. Projected entities for {projected_sentences} sentences out of {total_sentences}.")
    
    with open(output_path, "w", encoding="utf-8") as out_f:
        json.dump(training_data, out_f, ensure_ascii=False, indent=2)
        
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    project_ner_tags()
