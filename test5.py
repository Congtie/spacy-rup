from spacy_rup.orthography import to_cunia, to_diaro, detect_orthography

# Detectare
print(detect_orthography("Shi bună dzua"))  # "mixed"
print(detect_orthography("Shi bunã dzua"))  # "cunia"

# Conversie DIARO -> Cunia
text = "Și ńilji di oi"
print(to_cunia(text))  # "Shi njilji di oi"

# Conversie Cunia -> DIARO  
text = "Shi njilji di oi"
print(to_diaro(text))  # "Și ńiľi di oi"