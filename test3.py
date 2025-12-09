import spacy
nlp = spacy.blank('rup')
from spacy_rup.stop_words import STOP_WORDS

print("shi" in STOP_WORDS)  # True
print("ficior" in STOP_WORDS)  # False

# Filtrare
doc = nlp("Ficiorlu shi feata")
cuvinte_importante = [t for t in doc if t.text.lower() not in STOP_WORDS]