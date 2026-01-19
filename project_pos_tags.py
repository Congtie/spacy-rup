import spacy
from spacy.tokens import Doc
from pathlib import Path
from spacy_rup import Aromanian
import difflib

def project_tags():
    # Load Romanian model for tagging source text
    try:
        nlp_ro = spacy.load("ro_core_news_sm")
    except OSError:
        print("Error: ro_core_news_sm not found.")
        return

    # Initialize Aromanian nlp for tokenization
    # Disable other pipes for speed/purity
    nlp_rup = Aromanian()

    data_dir = Path("data")
    ro_path = data_dir / "Tales.train.ro"
    rup_path = data_dir / "Tales.train.rup"
    output_path = data_dir / "train.rup.conll"

    if not ro_path.exists() or not rup_path.exists():
        print(f"Error: Corpus files not found in {data_dir}")
        return

    print(f"Reading from {ro_path} and {rup_path}...")
    
    with open(ro_path, "r", encoding="utf-8") as f:
        ro_lines = f.readlines()
    with open(rup_path, "r", encoding="utf-8") as f:
        rup_lines = f.readlines()

    assert len(ro_lines) == len(rup_lines), "Corpus files must have same number of lines"

    projected_tokens = 0
    total_tokens_rup = 0
    
    with open(output_path, "w", encoding="utf-8") as out_f:
        for i, (ro_line, rup_line) in enumerate(zip(ro_lines, rup_lines)):
            ro_line = ro_line.strip()
            rup_line = rup_line.strip()
            
            if not ro_line or not rup_line:
                continue

            # Tag Romanian
            doc_ro = nlp_ro(ro_line)
            
            # Tokenize Aromanian
            doc_rup = nlp_rup(rup_line)
            
            ro_tokens = [t.text for t in doc_ro]
            rup_tokens = [t.text for t in doc_rup]
            total_tokens_rup += len(rup_tokens)

            # Use SequenceMatcher to align
            # We match on lowercased text to help with capitalization diffs
            matcher = difflib.SequenceMatcher(None, 
                [t.lower() for t in ro_tokens], 
                [t.lower() for t in rup_tokens]
            )
            
            # Get matching blocks: (ro_start, rup_start, length)
            # This identifies sub-sequences that match "exactly" (based on the input list)
            # BUT SequenceMatcher on lists checks equality of elements. 
            # ro "este" != rup "easte". So basic SequenceMatcher might fail on cognates.
            # We need a custom scoring or iterative approach.
            
            # Better approach for cognates:
            # 1. Use SequenceMatcher to find the "skeleton" of identical words (punctuation, names, common words)
            # 2. Fill in gaps?
            
            # Actually, let's trust SequenceMatcher to find the longest common subsequences.
            # Ideally "Ficiorlu a meu easte bun" vs "Feciorul meu este bun"
            # SequenceMatcher might align "meu", "bun", ".".
            
            # Let's try to iterate through opcodes to handle Replace/Equal
            opcodes = matcher.get_opcodes()
            
            # We will build a list of (rup_token, assigned_pos)
            # Initialize with None
            rup_tags = [None] * len(rup_tokens)
            
            for tag, i1, i2, j1, j2 in opcodes:
                if tag == 'equal':
                    # Direct match (identical words/punct)
                    for k in range(i2-i1):
                        # ro_tokens[i1+k] == rup_tokens[j1+k]
                        # Transfer tag
                        ro_idx = i1 + k
                        rup_idx = j1 + k
                        rup_tags[rup_idx] = doc_ro[ro_idx].pos_
                
                elif tag == 'replace':
                    # Block of words replaced by another block.
                    # e.g. ro: ["este"], rup: ["easte"]
                    # Check if they are cognates (similar strings)
                    # If 1-to-1 replacement, compare similarity
                    if (i2 - i1) == (j2 - j1) == 1:
                        ro_word = ro_tokens[i1]
                        rup_word = rup_tokens[j1]
                        
                        # Similarity check
                        sim = difflib.SequenceMatcher(None, ro_word.lower(), rup_word.lower()).ratio()
                        
                        # Thresholds:
                        # > 0.7 for words longer than 3 chars
                        # Exact match required for very short words if not covered by 'equal' (handled above)
                        if len(rup_word) > 3 and sim > 0.75:
                             rup_tags[j1] = doc_ro[i1].pos_
                        elif len(rup_word) <= 3 and sim > 0.8: # stricter for short words
                             rup_tags[j1] = doc_ro[i1].pos_
                    
            # Write only if we have some tax, but frankly we want sentences.
            # If we skip tokens, we can't train a sequence model well on that sentence 
            # unless we treat missing tags as 'X' or split sentences?
            # spaCy training supports missing tags? No, it expects a full Doc.
            # WE MUST PRESERVE SENTENCE STRUCTURE.
            # If we have gaps, we can either:
            # 1. Skip the whole sentence (Strict)
            # 2. Use a default tag (e.g. NOUN or X) -> Bad for training.
            # 3. Only Output sentences where ALL tokens are tagged.
            
            # Output even if partial, but maybe filter very sparse ones?
            # Let's verify we have at least ONE tag.
            if any(t is not None for t in rup_tags):
                for token_text, pos in zip(rup_tokens, rup_tags):
                     # Use '_' for missing tags (standard CoNLL practice for missing)
                     tag_str = pos if pos else "_"
                     out_f.write(f"{token_text}\t{tag_str}\n")
                out_f.write("\n")
                projected_tokens += len([t for t in rup_tags if t])
            else:
                # Optional: Log dropped sentences for debug?
                pass
                
    print(f"Done. Projected {projected_tokens} tokens out of total {total_tokens_rup} ({projected_tokens/total_tokens_rup:.1%} coverage).")
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    project_tags()
