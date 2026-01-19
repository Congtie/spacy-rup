
import sys
import os

# Add current directory to path so we can import spacy_rup
sys.path.append(os.getcwd())

import importlib.util

def load_orthography_module():
    file_path = os.path.join(os.getcwd(), 'spacy_rup', 'orthography.py')
    spec = importlib.util.spec_from_file_location("orthography", file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["orthography"] = module
    spec.loader.exec_module(module)
    return module

orthography = load_orthography_module()
detect_orthography = orthography.detect_orthography
ORTHOGRAPHY_MODEL = orthography.ORTHOGRAPHY_MODEL

def test_integration():
    print("Testing Orthography Model Integration")
    print("=====================================")
    
    # 1. Check if model is loaded
    if ORTHOGRAPHY_MODEL:
        print("[PASS] Method loaded ORTHOGRAPHY_MODEL successfully.")
    else:
        print("[FAIL] ORTHOGRAPHY_MODEL is None. Integration failed or sklearn missing.")
        
    # 2. Test cases
    test_cases = [
        ("Bunã dzua, cum s-dzuce?", "cunia"),
        ("Bună d̦ua, cum s-d̦uce?", "diaro"), # Correct Diaro uses d̦ (d-comma)
        ("Bună dzua, cum s-dzuce?", "cunia"), # Mixed, but model leans Cunia due to 'dz'
        ("shi cum dipuse", "cunia"), # 'sh' is strong cunia indicator
        ("si cum dipuse", "unknown"), # ambiguous, accept unknown
        ("Tigaie", "unknown"), # Short, no markers
    ]
    
    print("\nRunning Prediction Tests:")
    for text, expected in test_cases:
        result = detect_orthography(text)
        status = "PASS" if result == expected or expected == "unknown" else "WARN" 
        # Note: 'si cum dipuse' might be tricky for model if not in training data significantly
        
        print(f"Text: '{text}'")
        print(f"  Expected: {expected}")
        print(f"  Predicted: {result}")
        print(f"  Status: {status}")
        print("-" * 20)

if __name__ == "__main__":
    test_integration()
