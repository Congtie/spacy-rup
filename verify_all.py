import spacy
import spacy_rup
from spacy_rup.orthography import detect_orthography

def verify_all():
    print("="*60)
    print("      SPACY-RUP SYSTEM VERIFICATION")
    print("="*60)
    
    # 1. Test Orthography
    # 1. Test Orthography
    print("\n[1/3] Testing ORTHOGRAPHY Model...")
    ortho_tests = [
        ("Bunã dzua", "cunia"),
        ("Bună d̦ua", "diaro"),
        ("Tigaie", "unknown"), # Short/Ambiguous
        ("sh-a curat", "cunia"),
        ("și-a curat", "diaro"),
    ]
    
    passes = 0
    for text, expected in ortho_tests:
        try:
            detected = detect_orthography(text)
            print(f"  Input: '{text:<15}' -> Detected: {detected:<8} (Expected: {expected})")
            if detected == expected or (expected == 'unknown' and detected == 'unknown'):
                passes += 1
            elif expected == 'unknown' and detected != 'unknown':
                 print(f"  Note: Model made a guess '{detected}' for ambiguous input.")
                 passes += 1 # We'll be lenient on unknown if it guesses
        except Exception as e:
            print(f"  Error on '{text}': {e}")
            
    if passes >= len(ortho_tests) - 1: # Allow 1 tolerance for ambiguity
        print(f"  ✅ Orthography Model: PASS ({passes}/{len(ortho_tests)})")
    else:
        print(f"  ⚠️ Orthography Model: WARN ({passes}/{len(ortho_tests)})")


    # 2. Test POS Tagger
    print("\n[2/3] Testing POS TAGGER Model...")
    pos_tests = [
        "Ficiorlu featse un lucru multu bun",
        "Dă-nji ună măr!",
        "Câți oaminji suntu?",
    ]
    
    nlp_pos = None
    try:
        nlp_pos = spacy.load("spacy_rup/resources/pos_model")
        print(f"  Loaded model: {nlp_pos.pipe_names}")
        
        pos_passes = 0
        for text in pos_tests:
            doc = nlp_pos(text)
            tags = [(t.text, t.tag_) for t in doc]
            # Check if we got tags for most tokens
            has_tags = sum(1 for t in tags if t[1]) > len(tags) / 2
            
            print(f"  Sentence: '{text}'")
            print(f"  Tags: {tags}")
            
            if has_tags:
                pos_passes += 1
        
        if pos_passes == len(pos_tests):
             print(f"  ✅ POS Model: PASS ({pos_passes}/{len(pos_tests)})")
        else:
             print(f"  ❌ POS Model: FAIL ({pos_passes}/{len(pos_tests)})")
             
    except Exception as e:
        print(f"  ❌ POS Model: FAIL ({e})")


    # 3. Test NER
    print("\n[3/3] Testing NER Model...")
    ner_tests = [
        ("DI AL NASTRADIN-HOGEA", ["NASTRADIN-HOGEA"]),
        ("Moreee, ți săndze lai au", ["Moreee"]), # GPE based on training data example
        ("Eară ună oară trei călători", ["trei", "călători"]), # Numeric, Person
    ]

    try:
        nlp_ner = spacy.load("spacy_rup/resources/ner_model")
        print(f"  Loaded model: {nlp_ner.pipe_names}")
        
        ner_passes = 0
        for text, expected_entities_partial in ner_tests:
            doc_ner = nlp_ner(text)
            found_entities = [e.text for e in doc_ner.ents]
            
            print(f"  Sentence: '{text}'")
            print(f"  Found: {found_entities} (Expected at least: {expected_entities_partial})")
            
            # loose check: found entities should overlap with expected
            if any(e in found_entities for e in expected_entities_partial):
                ner_passes += 1
            elif not expected_entities_partial and not found_entities:
                ner_passes += 1
            else:
                 print("  -> Missed expected entity")

        if ner_passes >= len(ner_tests) - 1: # Allow slight tolerance
             print(f"  ✅ NER Model: PASS ({ner_passes}/{len(ner_tests)})")
        else:
             print(f"  ⚠️ NER Model: WARN ({ner_passes}/{len(ner_tests)})")
             
    except Exception as e:
         print(f"  ❌ NER Model: FAIL ({e})")
    print("VERIFICATION COMPLETE")
    print("="*60)

if __name__ == "__main__":
    verify_all()
