from spacy_rup.lex_attrs import like_num

print(like_num("trei"))   # True
print(like_num("dzatsi")) # True (zece)
print(like_num("casa"))   # False