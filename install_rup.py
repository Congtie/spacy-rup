"""
Script pentru instalarea modulului Aromanian (rup) în spaCy.
Copiază folderul spacy_rup/ în spacy/lang/rup/.
"""

import os
import sys
import shutil

def find_spacy_lang_dir():
    """Găsește directorul spacy/lang din instalarea spaCy."""
    try:
        import spacy
        spacy_path = os.path.dirname(spacy.__file__)
        lang_path = os.path.join(spacy_path, "lang")
        if os.path.exists(lang_path):
            return lang_path
        else:
            print(f"Eroare: Nu am găsit {lang_path}")
            return None
    except ImportError:
        print("Eroare: spaCy nu este instalat")
        return None


def install_rup_module():
    """Instalează modulul rup în spaCy."""
    # Calea către modulul sursă
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source_dir = os.path.join(script_dir, "spacy_rup")
    
    if not os.path.exists(source_dir):
        print(f"Eroare: Nu am găsit {source_dir}")
        return False
    
    # Găsește directorul spacy/lang
    lang_dir = find_spacy_lang_dir()
    if not lang_dir:
        return False
    
    # Calea destinație
    target_dir = os.path.join(lang_dir, "rup")
    
    print(f"Sursă: {source_dir}")
    print(f"Destinație: {target_dir}")
    
    # Verifică dacă există deja
    if os.path.exists(target_dir):
        response = input(f"\n{target_dir} există deja. Suprascriu? (y/n): ")
        if response.lower() != 'y':
            print("Anulat.")
            return False
        shutil.rmtree(target_dir)
    
    # Copiază directorul
    try:
        shutil.copytree(source_dir, target_dir)
        print(f"\n✓ Modulul a fost copiat în {target_dir}")
    except Exception as e:
        print(f"\nEroare la copiere: {e}")
        return False
    
    # Test import
    print("\nTestez importul...")
    try:
        # Reimportăm spacy pentru a detecta noul modul
        import importlib
        import spacy
        importlib.reload(spacy)
        
        from spacy.lang.rup import Aromanian
        nlp = Aromanian()
        
        doc = nlp("Bunã dzua! Mini hiu armãn.")
        tokens = [t.text for t in doc]
        print(f"✓ Import reușit!")
        print(f"  Test: 'Bunã dzua! Mini hiu armãn.' -> {tokens}")
        
        return True
        
    except ImportError as e:
        print(f"⚠ Eroare import: {e}")
        print("  Poate fi necesar să repornești Python pentru a detecta noul modul.")
        return True  # Copierea a reușit, doar importul imediat nu merge
    
    return True


def uninstall_rup_module():
    """Dezinstalează modulul rup din spaCy."""
    lang_dir = find_spacy_lang_dir()
    if not lang_dir:
        return False
    
    target_dir = os.path.join(lang_dir, "rup")
    
    if not os.path.exists(target_dir):
        print(f"Modulul nu este instalat în {target_dir}")
        return False
    
    try:
        shutil.rmtree(target_dir)
        print(f"✓ Modulul a fost șters din {target_dir}")
        return True
    except Exception as e:
        print(f"Eroare la ștergere: {e}")
        return False


def main():
    print("=" * 60)
    print("  INSTALARE MODUL AROMANIAN (rup) ÎN SPACY")
    print("=" * 60)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--uninstall":
        uninstall_rup_module()
    else:
        success = install_rup_module()
        
        if success:
            print("\n" + "=" * 60)
            print("  INSTALARE COMPLETĂ!")
            print("=" * 60)
            print("\nPoți folosi modulul astfel:")
            print("  from spacy.lang.rup import Aromanian")
            print("  nlp = Aromanian()")
            print("  doc = nlp('Bunã dzua!')")
            print("\nSau cu spacy.blank:")
            print("  import spacy")
            print("  nlp = spacy.blank('rup')")
        else:
            print("\nInstalarea a eșuat.")


if __name__ == "__main__":
    main()
