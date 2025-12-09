import spacy

nlp = spacy.blank('rup')
doc = nlp("Ficiorlu s-dutse tu munte.")

for token in doc:
    print(token.text)
# Ficiorlu, s-, dutse, tu, munte, .