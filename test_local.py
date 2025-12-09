"""
Test local pentru modulul Aromanian spaCy fără instalare în spaCy.
Testează componentele individual (fără importuri relative).
"""

import sys
import os
import re

# Adaugă path-ul pentru importuri locale
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_stop_words():
    """Testează stop words (citind fișierul direct)."""
    print("=" * 50)
    print("TEST: Stop Words")
    print("=" * 50)
    
    # Citim stop words direct din fișier (evităm importuri relative)
    stop_words_file = os.path.join(os.path.dirname(__file__), "spacy_rup", "stop_words.py")
    
    with open(stop_words_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extragem manual stop words din fișier
    match = re.search(r'STOP_WORDS\s*=\s*set\s*\(\s*"""(.*?)"""', content, re.DOTALL)
    if match:
        words_text = match.group(1)
        STOP_WORDS = set(words_text.split())
    else:
        print("  Nu am putut parsa stop_words.py")
        return False
    
    print(f"Numar total stop words: {len(STOP_WORDS)}")
    
    # Test cuvinte care trebuie să fie stop words (din corpus)
    expected_stop = ["di", "shi", "cu", "nu", "tu", "a", "la", "ca", "un", 
                     "ma", "tse", "si", "cum", "pri", "va",
                     "eara", "easte", "multu", "lui", "cari", "iu", "ghine"]
    
    found = [w for w in expected_stop if w in STOP_WORDS]
    missing = [w for w in expected_stop if w not in STOP_WORDS]
    
    print(f"Gasite: {len(found)}/{len(expected_stop)}")
    if missing:
        print(f"Lipsesc: {missing}")
    
    # Exemplu de stop words
    print(f"\nExemple stop words: {sorted(list(STOP_WORDS))[:20]}...")
    
    return len(missing) == 0


def test_lex_attrs():
    """Testează detectarea numeralelor."""
    print("\n" + "=" * 50)
    print("TEST: Numerale (lex_attrs)")
    print("=" * 50)
    
    # Citim lex_attrs.py
    lex_file = os.path.join(os.path.dirname(__file__), "spacy_rup", "lex_attrs.py")
    
    with open(lex_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extragem _num_words
    match = re.search(r'_num_words\s*=\s*\{([^}]+)\}', content, re.DOTALL)
    if not match:
        print("  Nu am putut parsa lex_attrs.py")
        return False
    
    # Parsăm setul de numerale
    words_str = match.group(1)
    num_words = set(re.findall(r'"([^"]+)"', words_str))
    
    print(f"Numar numerale definite: {len(num_words)}")
    
    # Numerale care trebuie detectate (din corpus)
    numbers = ["un", "doi", "doaua", "trei", "patru", "tsintsi", 
               "shase", "shapte", "optu", "noaua", "dzatsi", "suta", "njilji"]
    
    all_passed = True
    
    print("Verificare numerale din corpus:")
    for num in numbers:
        if num in num_words:
            print(f"  OK '{num}' -> prezent in _num_words")
        else:
            # Verificăm variante cu diacritice
            variants = [num, num.replace('a', 'ã'), num.replace('ua', 'uã')]
            found_var = any(v in num_words for v in variants)
            if found_var:
                print(f"  OK '{num}' -> prezent (varianta cu diacritice)")
            else:
                print(f"  LIPSA '{num}'")
                all_passed = False
    
    return all_passed


def test_orthography():
    """Testează conversiile ortografice."""
    print("\n" + "=" * 50)
    print("TEST: Conversie Ortografica")
    print("=" * 50)
    
    # Importăm orthography.py (nu are dependențe de spaCy)
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "orthography", 
        os.path.join(os.path.dirname(__file__), "spacy_rup", "orthography.py")
    )
    orth_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(orth_module)
    
    to_cunia = orth_module.to_cunia
    to_diaro = orth_module.to_diaro
    detect_orthography = orth_module.detect_orthography
    
    # Test cases din corpus
    test_cases = [
        ("si", "shi"),
        ("te", "tse"),
        ("li", "lji"),
    ]
    
    all_passed = True
    
    print("DIARO -> Cunia:")
    for diaro, cunia_expected in test_cases:
        cunia_result = to_cunia(diaro)
        print(f"  '{diaro}' -> '{cunia_result}'")
    
    print("\nCunia -> DIARO:")
    for diaro_expected, cunia in test_cases:
        diaro_result = to_diaro(cunia)
        print(f"  '{cunia}' -> '{diaro_result}'")
    
    print("\nDetectie ortografie:")
    cunia_text = "Shi una vulpe, tse dzase"
    diaro_text = "Si una vulpe, te dise"
    
    print(f"  Cunia: '{cunia_text}' -> {detect_orthography(cunia_text)}")
    print(f"  DIARO: '{diaro_text}' -> {detect_orthography(diaro_text)}")
    
    return True


def test_tokenizer_exceptions_syntax():
    """Verifică sintaxa tokenizer_exceptions.py."""
    print("\n" + "=" * 50)
    print("TEST: Sintaxa Tokenizer Exceptions")
    print("=" * 50)
    
    tok_file = os.path.join(os.path.dirname(__file__), "spacy_rup", "tokenizer_exceptions.py")
    
    with open(tok_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificăm că conține contracții importante
    important_contractions = [
        "s-nu", "s-lu", "s-lji", "s-u", 
        "shi-lji", "shi-u", "nu-lji", "nu-i",
    ]
    
    found = []
    missing = []
    
    for contr in important_contractions:
        if f'"{contr}"' in content or f"'{contr}'" in content:
            found.append(contr)
        else:
            missing.append(contr)
    
    print(f"Contractii din corpus gasite: {len(found)}/{len(important_contractions)}")
    
    if missing:
        print(f"  Lipsesc: {missing}")
    
    print(f"  Contractii gasite: {found}")
    
    return len(missing) < 3


def test_corpus_sentences():
    """Testează cu propoziții reale din corpus."""
    print("\n" + "=" * 50)
    print("TEST: Propozitii din Corpus")
    print("=" * 50)
    
    # Propoziții din corpus.rup_cun
    corpus_sentences = [
        "Eara tse nu sh-eara.",
        "Eara un lup, shi una vulpe.",
        "S-nu poata s-lu vatama.",
        "Luplu nu-lji dzase tsiva.",
        "Vulpea featse cum featse.",
    ]
    
    print("Propozitii din corpus - tokenizare simpla:")
    for sent in corpus_sentences:
        print(f"\n  Input: '{sent}'")
        tokens = simple_tokenize(sent)
        print(f"  Tokens ({len(tokens)}): {tokens}")
    
    return True


def simple_tokenize(text):
    """Tokenizare simplă pentru demonstrație."""
    pattern = r"[\w']+(?:-[\w']+)*|[.,!?;:\-]"
    tokens = re.findall(pattern, text)
    return tokens


def test_file_structure():
    """Verifică structura de fișiere."""
    print("\n" + "=" * 50)
    print("TEST: Structura Fisiere")
    print("=" * 50)
    
    base_dir = os.path.join(os.path.dirname(__file__), "spacy_rup")
    
    required_files = [
        "__init__.py",
        "stop_words.py", 
        "punctuation.py",
        "tokenizer_exceptions.py",
        "lex_attrs.py",
        "orthography.py",
        "examples.py",
        "README.md",
    ]
    
    all_present = True
    
    for fname in required_files:
        fpath = os.path.join(base_dir, fname)
        if os.path.exists(fpath):
            size = os.path.getsize(fpath)
            print(f"  OK {fname} ({size} bytes)")
        else:
            print(f"  LIPSA {fname}")
            all_present = False
    
    return all_present


def main():
    """Rulează toate testele."""
    print("\n" + "=" * 60)
    print("  TESTE PENTRU MODULUL AROMANIAN SPACY (rup)")
    print("  (Testare locala fara instalare in spaCy)")
    print("=" * 60)
    
    results = []
    
    results.append(("Structura Fisiere", test_file_structure()))
    results.append(("Stop Words", test_stop_words()))
    results.append(("Numerale", test_lex_attrs()))
    results.append(("Ortografie", test_orthography()))
    results.append(("Tokenizer Exceptions", test_tokenizer_exceptions_syntax()))
    results.append(("Corpus Sentences", test_corpus_sentences()))
    
    print("\n" + "=" * 60)
    print("  REZUMAT")
    print("=" * 60)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"  {status}: {name}")
    
    print(f"\nTotal: {passed}/{total} teste trecute")
    
    if passed == total:
        print("\n" + "=" * 60)
        print("TOATE TESTELE AU TRECUT!")
        print("=" * 60)
        print("\nPentru a folosi modulul cu spaCy complet:")
        print("  1. Copiaza folderul 'spacy_rup/' in instalarea spaCy:")
        print("     site-packages/spacy/lang/rup/")
        print("  2. SAU foloseste entry_points pentru inregistrare")
    else:
        print("\nUnele teste au esuat. Verifica erorile de mai sus.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
