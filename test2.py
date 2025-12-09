import spacy

nlp = spacy.blank('rup')
nlp.add_pipe('aromanian_lemmatizer')

doc = nlp("Ficiorlu featse un lucru.")
for token in doc:
    print(f"{token.text:12} -> {token.lemma_}")
# Ficiorlu     -> ficior
# featse       -> fac