import spacy
from pathlib import Path
from spacy.pipeline import AttributeRuler
import spacy_rup
from spacy_rup.lemmatizer import VERB_LEMMAS, NOUN_LEMMAS, ADJ_LEMMAS, VERB_RULES, ADJ_RULES

def enrich_model():
    model_path = Path("spacy_rup/resources/pos_model")
    if not model_path.exists():
        print(f"Error: Model not found at {model_path}")
        return

    print(f"Loading model from {model_path}...")
    try:
        nlp = spacy.load(model_path)
    except Exception as e:
        print(f"Failed to load model: {e}")
        return

    # Add AttributeRuler
    # If it exists, remove it to start fresh? Or just get it.
    if "attribute_ruler" in nlp.pipe_names:
        ruler = nlp.get_pipe("attribute_ruler")
    else:
        # Add after tagger
        ruler = nlp.add_pipe("attribute_ruler", after="tagger")

    print("Adding rules from lemmatizer dictionaries...")
    
    # Verbs
    # Map both keys (forms) and values (lemmas) to VERB per se? 
    # Usually keys are inflected forms.
    # Note: Some words might be ambiguous. We trust the lists for now.
    # VERB_LEMMAS keys are like "hiu", "eshti".
    # Should check for collision?
    
    verb_patterns = [{"ORTH": word} for word in VERB_LEMMAS.keys()]
    # ruler.add expects patterns as a list of lists of dicts (each inner list is a pattern for a token sequence)
    # BUT actually ruler.add(patterns=[...]) takes a LIST of patterns.
    # Each pattern is a LIST of dicts.
    # So if we want to match single words, we need [[{"ORTH": "word1"}], [{"ORTH": "word2"}]]?
    # No, let's follow the docs. patterns=[[{"ORTH": "word"}]] matches one token "word".
    
    # Let's fix the loops below.
    
    pass

    # Let's be specific for AUX candidates
    aux_lemmas = ["hiu", "am", "vrea", "potu"] # be, have, want, can
    
    verb_forms = []
    aux_forms = []
    
    # Add lemma forms as well
    for lemma in VERB_LEMMAS.values():
         if lemma in aux_lemmas and lemma not in aux_forms:
             aux_forms.append(lemma)
         elif lemma not in aux_lemmas and lemma not in verb_forms:
             verb_forms.append(lemma)
             
    # De-duplicate
    verb_forms = list(set(verb_forms))
    aux_forms = list(set(aux_forms))

    if aux_forms:
        ruler.add(patterns=[[{"LOWER": w}] for w in aux_forms], attrs={"POS": "AUX", "TAG": "AUX"})
    if verb_forms:
        ruler.add(patterns=[[{"LOWER": w}] for w in verb_forms], attrs={"POS": "VERB", "TAG": "VERB"})

    # Adjectives
    adj_forms = list(ADJ_LEMMAS.keys()) + list(ADJ_LEMMAS.values())
    adj_forms = list(set(adj_forms))
    if adj_forms:
        ruler.add(patterns=[[{"LOWER": w}] for w in adj_forms], attrs={"POS": "ADJ", "TAG": "ADJ"})

    # Nouns
    noun_forms = list(NOUN_LEMMAS.keys()) + list(NOUN_LEMMAS.values())
    noun_forms = list(set(noun_forms))
    if noun_forms:
        ruler.add(patterns=[[{"LOWER": w}] for w in noun_forms], attrs={"POS": "NOUN", "TAG": "NOUN"})
        
    # Manual fixes for things not in lists or ambiguous
    manual_rules = {
        "tu": "ADP", # defaulting to 'in'
        "di": "ADP",
        "la": "ADP",
        "cu": "ADP",
        "pi": "ADP",
        "tră": "ADP",
        "și": "CCONJ",
        "i": "CCONJ",
        "ma": "CCONJ",
        "că": "SCONJ",
        "un": "DET",
        "ună": "DET",
        "nă": "DET", # Short for ună
        ".": "PUNCT",
        ",": "PUNCT",
        "?": "PUNCT",
        "!": "PUNCT",
        "buni": "ADJ",
        "mărșește": "VERB",
        "aicea": "ADV",
        
        # New additions for enhanced coverage
        "yină": "VERB",
        "mâni": "ADV",
        "aist": "DET",
        "ari": "AUX",
        "faci": "VERB",
        "măc": "VERB",
        "dudau": "NOUN",
        "ți": "PRON",
        "va": "AUX", # Future particle
        
        # Latest additions
        "dă-nji": "VERB", # Treat as verb for now
        "măr": "NOUN",
        "fugă": "VERB",
        "câți": "DET",
        "mine": "PRON",
        "tău": "DET",
        "escu": "AUX",
        "poati": "AUX",
    }
    
    for word, pos in manual_rules.items():
        ruler.add(patterns=[[{"LOWER": word}]], attrs={"POS": pos, "TAG": pos})

    print(f"Added rules for {len(aux_forms)} AUX, {len(verb_forms)} VERB, {len(adj_forms)} ADJ, {len(noun_forms)} NOUN, and {len(manual_rules)} manual items.")
    
    nlp.to_disk(model_path)
    print(f"Saved enriched model to {model_path}")

if __name__ == "__main__":
    enrich_model()
