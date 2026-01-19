
import sys
import os
from pathlib import Path
import json


# Add local path to test without installing
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


# Add local path to test without installing
import importlib.util
spec = importlib.util.spec_from_file_location(
    "orthography", 
    os.path.join(os.path.dirname(__file__), "spacy_rup", "orthography.py")
)
orth_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(orth_module)

detect_orthography = orth_module.detect_orthography
cunia_to_diaro = orth_module.cunia_to_diaro
to_diaro = orth_module.to_diaro
FREQ_AH = orth_module.FREQ_AH
FREQ_UH = orth_module.FREQ_UH

def test_final_implementation():
    print("=" * 60)
    print("TESTING ARO MODEL AND FINAL TRANSLATOR")
    print("=" * 60)
    
    # 1. Test Detection (Aro Model)
    print("\n[1] Testing Detection (Aro Model)")
    test_cases_detection = [
        ("Bunã dzua, cum s-dzuce?", "cunia"),
        ("Bună dzua, cum s-dzuce?", "diaro"),
        ("Eara un omu.", "unknown"), # ambiguous without specific markers
        ("Și ași s-face.", "diaro"),
    ]
    
    for text, expected in test_cases_detection:
        result = detect_orthography(text)
        status = "PASS" if result == expected else "FAIL"
        print(f"  [{status}] '{text}' -> Detected: {result} | Expected: {expected}")

    # 2. Test Translation with Frequency Maps (Final Translator)
    print("\n[2] Testing Translation with Frequency Maps")
    
    # Check if maps are loaded
    # from spacy_rup.orthography import FREQ_AH, FREQ_UH
    print(f"  Frequency maps size: 'â': {len(FREQ_AH)}, 'ă': {len(FREQ_UH)}")
    
    if not FREQ_AH or not FREQ_UH:
        print("  WARNING: Frequency maps are empty! Translation will be suboptimal.")
    
    # Specific words that need context or valid dictionary lookups
    # "cântic" (song) vs "căn" (mug/can - rare/improbable in aro context but good for testing differentiation)
    # Better test: standard words known to use 'â' vs 'ă'
    # "până" (until) -> "pãnã" in Cunia. "până" in Diaro.
    # "drapăl" (flag) -> "drapãl".
    
    # Let's try some sentences from the corpus if possible, or common phrases
    test_cases_translation = [
        ("pãnã", "până"),   # â check
        ("mãna", "mâna"),   # â check (hand)
        ("una", "una"),     # a check (unchanged)
        ("cãntic", "cântic"), # â check
        ("bunã", "bună"),   # ă check (good - fem)
    ]
    
    for inp, expected in test_cases_translation:
        # Note: input here is Cunia or simple string.
        # But wait, 'una' doesn't have 'ã'.
        # 'pãnã' has two 'ã'.
        
        # We need to simulate the context window relative to the 'ã'.
        # The translator runs on full text.
        
        out = cunia_to_diaro(inp)
        print(f"  '{inp}' -> '{out}' (Expected: '{expected}')")
        
    print("\n[3] Full Sentence Translation")
    sentence_cunia = "Unã oarã eara unã vulpe."
    sentence_diaro = cunia_to_diaro(sentence_cunia)
    print(f"  Cunia: {sentence_cunia}")
    print(f"  Diaro: {sentence_diaro}")
    
    # Expected: "Ună oară eara ună vulpe." (likely)
    
if __name__ == "__main__":
    test_final_implementation()
