

from spacy.symbols import ORTH, NORM
from spacy.util import update_exc
from spacy.lang.tokenizer_exceptions import BASE_EXCEPTIONS
from .punctuation import _make_rup_variants

_exc = {}

for orth in [
    "1-a",
    "2-a",
    "3-a",
    "4-a",
    "5-a",
    "6-a",
    "7-a",
    "8-a",
    "9-a",
    "10-a",
    "11-a",
    "12-a",
    "1-lu",
    "2-lea",
    "3-lea",
    "4-lea",
    "5-lea",
    "6-lea",
    "7-lea",
    "8-lea",
    "9-lea",
    "10-lea",
    "11-lea",
    "12-lea",
]:
    _exc[orth] = [{ORTH: orth}]

_aromanian_abbrevs = [
    "d-lu",
    "d-na",
    "d-ta",
    "d-voastã",
    "dvs.",
    "etc.",
    "nr.",
    "pag.",
    "vol.",
    "cap.",
    "sec.",
    "min.",
    "h.",
    "m.",
    "km.",
    "sf.",
    "St.",
    "prof.",
    "dr.",
    "ing.",
    "arm.",
    "rom.",
    "gr.",
]

for orth in _aromanian_abbrevs:
    _exc[orth] = [{ORTH: orth}]
    _exc[orth.capitalize()] = [{ORTH: orth.capitalize()}]


_contractions = [
    ("s-nu", [{ORTH: "s-"}, {ORTH: "nu"}]),
    ("S-nu", [{ORTH: "S-"}, {ORTH: "nu"}]),
    ("s-lu", [{ORTH: "s-"}, {ORTH: "lu"}]),
    ("s-lji", [{ORTH: "s-"}, {ORTH: "lji"}]),
    ("s-u", [{ORTH: "s-"}, {ORTH: "u"}]),
    ("s-hibã", [{ORTH: "s-"}, {ORTH: "hibã"}]),
    ("s-facã", [{ORTH: "s-"}, {ORTH: "facã"}]),
    ("S-mi", [{ORTH: "S-"}, {ORTH: "mi"}]),
    ("s-mi", [{ORTH: "s-"}, {ORTH: "mi"}]),
    ("s-nji", [{ORTH: "s-"}, {ORTH: "nji"}]),
    ("s-yinã", [{ORTH: "s-"}, {ORTH: "yinã"}]),
    ("S-featse", [{ORTH: "S-"}, {ORTH: "featse"}]),
    ("s-tsã", [{ORTH: "s-"}, {ORTH: "tsã"}]),
    ("s-ti", [{ORTH: "s-"}, {ORTH: "ti"}]),
    ("s-ducã", [{ORTH: "s-"}, {ORTH: "ducã"}]),
    ("s-lã", [{ORTH: "s-"}, {ORTH: "lã"}]),
    ("s-veadã", [{ORTH: "s-"}, {ORTH: "veadã"}]),
    ("s-turnã", [{ORTH: "s-"}, {ORTH: "turnã"}]),
    ("s-vã", [{ORTH: "s-"}, {ORTH: "vã"}]),
    ("s-ljea", [{ORTH: "s-"}, {ORTH: "ljea"}]),
    ("s-mãcã", [{ORTH: "s-"}, {ORTH: "mãcã"}]),
    ("s-li", [{ORTH: "s-"}, {ORTH: "li"}]),
    
    ("shi-lji", [{ORTH: "shi"}, {ORTH: "-"}, {ORTH: "lji"}]),
    ("shi-u", [{ORTH: "shi"}, {ORTH: "-"}, {ORTH: "u"}]),
    ("shi-l", [{ORTH: "shi"}, {ORTH: "-"}, {ORTH: "l"}]),
    ("shi-a", [{ORTH: "shi"}, {ORTH: "-"}, {ORTH: "a"}]),
    ("shi-shi", [{ORTH: "shi"}, {ORTH: "-"}, {ORTH: "shi"}]),
    
    ("si-lji", [{ORTH: "si"}, {ORTH: "-"}, {ORTH: "lji"}]),
    ("si-u", [{ORTH: "si"}, {ORTH: "-"}, {ORTH: "u"}]),
    ("si-shi", [{ORTH: "si"}, {ORTH: "-"}, {ORTH: "shi"}]),
    ("si-nji", [{ORTH: "si"}, {ORTH: "-"}, {ORTH: "nji"}]),
    ("si-l", [{ORTH: "si"}, {ORTH: "-"}, {ORTH: "l"}]),
    
    ("sh-u", [{ORTH: "sh-"}, {ORTH: "u"}]),
    ("sh-nu", [{ORTH: "sh-"}, {ORTH: "nu"}]),
    ("sh-io", [{ORTH: "sh-"}, {ORTH: "io"}]),
    ("sh-di", [{ORTH: "sh-"}, {ORTH: "di"}]),
    ("Sh-cu", [{ORTH: "Sh-"}, {ORTH: "cu"}]),
    ("sh-cu", [{ORTH: "sh-"}, {ORTH: "cu"}]),
    
    ("nu-lji", [{ORTH: "nu"}, {ORTH: "-"}, {ORTH: "lji"}]),
    ("nu-i", [{ORTH: "nu"}, {ORTH: "-"}, {ORTH: "i"}]),
    ("nu-nji", [{ORTH: "nu"}, {ORTH: "-"}, {ORTH: "nji"}]),
    ("nu-are", [{ORTH: "nu"}, {ORTH: "-"}, {ORTH: "are"}]),
    ("nu-avea", [{ORTH: "nu"}, {ORTH: "-"}, {ORTH: "avea"}]),
    
    ("lji-u", [{ORTH: "lji"}, {ORTH: "-"}, {ORTH: "u"}]),
    ("va-lji", [{ORTH: "va"}, {ORTH: "-"}, {ORTH: "lji"}]),
    ("tse-lji", [{ORTH: "tse"}, {ORTH: "-"}, {ORTH: "lji"}]),
    
    ("mã-sa", [{ORTH: "mã-sa"}]),
    ("tatã-su", [{ORTH: "tatã-su"}]),
    ("frate-su", [{ORTH: "frate-su"}]),
    ("sor-sa", [{ORTH: "sor-sa"}]),
    
    ("de-amirã", [{ORTH: "de"}, {ORTH: "-"}, {ORTH: "amirã"}]),
    ("de-a", [{ORTH: "de"}, {ORTH: "-"}, {ORTH: "a"}]),
    
    ("D-iu", [{ORTH: "D-"}, {ORTH: "iu"}]),
    ("d-iu", [{ORTH: "d-"}, {ORTH: "iu"}]),
    
    ("du-te", [{ORTH: "du"}, {ORTH: "-"}, {ORTH: "te"}]),
    
    ("n-are", [{ORTH: "n-"}, {ORTH: "are"}]),
    ("n-avem", [{ORTH: "n-"}, {ORTH: "avem"}]),
    ("n-avea", [{ORTH: "n-"}, {ORTH: "avea"}]),
    
    ("dintr-un", [{ORTH: "dintr-"}, {ORTH: "un"}]),
    ("dintr-una", [{ORTH: "dintr-"}, {ORTH: "una"}]),
]

for orth, expansion in _contractions:
    _exc[orth] = expansion

_greek_loans = [
    "efharisto",
    "kalimera",
    "kalispera",
    "parakalo",
    "adio",
    "thkiavaso",
]

for word in _greek_loans:
    _exc[word] = [{ORTH: word}]

_particles = [
    "cama",
    "mashi",
    "ninga",
    "tsiva",
    "ghine",
    "multu",
    "tora",
    "aclo",
    "escu",
    "vahi",
    "mãrã",
    "ehei",
    "bre",
    "apoia",
]

for particle in _particles:
    _exc[particle] = [{ORTH: particle}]

_apostrophe_words = [
    "l'i",
    "l'imba",
    "l'imbã",
    "l'ipidu",
    "n'",
    "n'i",
]

for word in _apostrophe_words:
    _exc[word] = [{ORTH: word}]

TOKENIZER_EXCEPTIONS = update_exc(BASE_EXCEPTIONS, _exc)



