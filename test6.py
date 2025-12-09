import spacy
from spacy_rup.orthography import to_cunia
from spacy_rup.stop_words import STOP_WORDS

# Creare pipeline
nlp = spacy.blank('rup')
nlp.add_pipe('aromanian_lemmatizer')

# Text în DIARO
text_diaro = "Ficiorlu și feata avură ńilji di oi."

# Convertește la Cunia
text_cunia = to_cunia(text_diaro)
print(f"Cunia: {text_cunia}")

# Procesare
doc = nlp(text_cunia)

# Afișare rezultate
print("\nToken -> Lemă -> Stop word?")
for token in doc:
    is_stop = "DA" if token.text.lower() in STOP_WORDS else ""
    print(f"  {token.text:12} -> {token.lemma_:12} {is_stop}")