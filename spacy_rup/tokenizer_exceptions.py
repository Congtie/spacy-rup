# Tokenizer exceptions for Aromanian
# Based on Romanian exceptions with Aromanian-specific additions

from ...symbols import ORTH, NORM
from ...util import update_exc
from ..tokenizer_exceptions import BASE_EXCEPTIONS
from .punctuation import _make_rup_variants

_exc = {}

# Ordinal number exceptions (like Romanian)
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

# Aromanian-specific abbreviations
_aromanian_abbrevs = [
    # Titles
    "d-lu",    # domnul (Mr.)
    "d-na",    # doamna (Mrs.)
    "d-ta",    # dumneata (you formal)
    "d-voastã",  # dumneavoastră
    "dvs.",
    # Common abbreviations
    "etc.",
    "nr.",
    "pag.",
    "vol.",
    "cap.",
    "sec.",
    "min.",
    "h.",
    # Geographic
    "m.",
    "km.",
    # Religious/cultural
    "sf.",
    "St.",
    # Academic
    "prof.",
    "dr.",
    "ing.",
    # Aromanian-specific
    "arm.",  # armãneashti
    "rom.",  # romãneashti
    "gr.",   # greceashti
]

for orth in _aromanian_abbrevs:
    _exc[orth] = [{ORTH: orth}]
    # Add capitalized version
    _exc[orth.capitalize()] = [{ORTH: orth.capitalize()}]

# Note: Multi-word expressions are NOT supported in spaCy tokenizer exceptions
# They should be handled by the Matcher or EntityRuler instead
# Example MWEs for future reference:
#   "tu soni" (finally), "di arada" (usually), "ma multu" (more)
#   "ma putsãn" (less), "cãt ma" (as...as), "shi cã" (and that)

# Contractions and clitics - based on corpus analysis (senisioi/aromanian)
# Most frequent patterns from corpus.rup_cun analysis:
_contractions = [
    # s-/si-/sh- prefix (reflexive/subjunctive) - MOST COMMON
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
    
    # shi- prefix + clitics
    ("shi-lji", [{ORTH: "shi"}, {ORTH: "-"}, {ORTH: "lji"}]),
    ("shi-u", [{ORTH: "shi"}, {ORTH: "-"}, {ORTH: "u"}]),
    ("shi-l", [{ORTH: "shi"}, {ORTH: "-"}, {ORTH: "l"}]),
    ("shi-a", [{ORTH: "shi"}, {ORTH: "-"}, {ORTH: "a"}]),
    ("shi-shi", [{ORTH: "shi"}, {ORTH: "-"}, {ORTH: "shi"}]),
    
    # si- prefix + clitics
    ("si-lji", [{ORTH: "si"}, {ORTH: "-"}, {ORTH: "lji"}]),
    ("si-u", [{ORTH: "si"}, {ORTH: "-"}, {ORTH: "u"}]),
    ("si-shi", [{ORTH: "si"}, {ORTH: "-"}, {ORTH: "shi"}]),
    ("si-nji", [{ORTH: "si"}, {ORTH: "-"}, {ORTH: "nji"}]),
    ("si-l", [{ORTH: "si"}, {ORTH: "-"}, {ORTH: "l"}]),
    
    # sh- prefix + clitics (variant of shi-)
    ("sh-u", [{ORTH: "sh-"}, {ORTH: "u"}]),
    ("sh-nu", [{ORTH: "sh-"}, {ORTH: "nu"}]),
    ("sh-io", [{ORTH: "sh-"}, {ORTH: "io"}]),
    ("sh-di", [{ORTH: "sh-"}, {ORTH: "di"}]),
    ("Sh-cu", [{ORTH: "Sh-"}, {ORTH: "cu"}]),
    ("sh-cu", [{ORTH: "sh-"}, {ORTH: "cu"}]),
    
    # nu- negation + clitics
    ("nu-lji", [{ORTH: "nu"}, {ORTH: "-"}, {ORTH: "lji"}]),
    ("nu-i", [{ORTH: "nu"}, {ORTH: "-"}, {ORTH: "i"}]),
    ("nu-nji", [{ORTH: "nu"}, {ORTH: "-"}, {ORTH: "nji"}]),
    ("nu-are", [{ORTH: "nu"}, {ORTH: "-"}, {ORTH: "are"}]),
    ("nu-avea", [{ORTH: "nu"}, {ORTH: "-"}, {ORTH: "avea"}]),
    
    # lji-u compound clitics
    ("lji-u", [{ORTH: "lji"}, {ORTH: "-"}, {ORTH: "u"}]),
    ("va-lji", [{ORTH: "va"}, {ORTH: "-"}, {ORTH: "lji"}]),
    ("tse-lji", [{ORTH: "tse"}, {ORTH: "-"}, {ORTH: "lji"}]),
    
    # Possessive forms
    ("mã-sa", [{ORTH: "mã-sa"}]),  # his/her mother
    ("tatã-su", [{ORTH: "tatã-su"}]),  # his father
    ("frate-su", [{ORTH: "frate-su"}]),  # his brother
    ("sor-sa", [{ORTH: "sor-sa"}]),  # his/her sister
    
    # de-amirã compound
    ("de-amirã", [{ORTH: "de"}, {ORTH: "-"}, {ORTH: "amirã"}]),
    ("de-a", [{ORTH: "de"}, {ORTH: "-"}, {ORTH: "a"}]),
    
    # D-iu (de + iu = where from)
    ("D-iu", [{ORTH: "D-"}, {ORTH: "iu"}]),
    ("d-iu", [{ORTH: "d-"}, {ORTH: "iu"}]),
    
    # du-te imperative
    ("du-te", [{ORTH: "du"}, {ORTH: "-"}, {ORTH: "te"}]),
    
    # n- prefix (negative/locative)
    ("n-are", [{ORTH: "n-"}, {ORTH: "are"}]),
    ("n-avem", [{ORTH: "n-"}, {ORTH: "avem"}]),
    ("n-avea", [{ORTH: "n-"}, {ORTH: "avea"}]),
    
    # dintr- preposition
    ("dintr-un", [{ORTH: "dintr-"}, {ORTH: "un"}]),
    ("dintr-una", [{ORTH: "dintr-"}, {ORTH: "una"}]),
]

for orth, expansion in _contractions:
    _exc[orth] = expansion
    # Note: Orthographic variants would need matching expansions
    # For now, we only include the base forms

# Greek-influenced words that should not be split
_greek_loans = [
    "efharisto",  # thank you (ευχαριστώ)
    "kalimera",   # good morning
    "kalispera",  # good evening
    "parakalo",   # please
    "adio",       # goodbye
    "thkiavaso",  # I read
]

for word in _greek_loans:
    _exc[word] = [{ORTH: word}]

# Aromanian-specific particles and function words - from corpus
_particles = [
    # Common function words (top frequency)
    "cama",   # more
    "mashi",  # only
    "ninga",  # still
    "tsiva",  # something
    "ghine",  # well
    "multu",  # much
    "tora",   # now
    "aclo",   # there
    # Question particles
    "escu",
    "vahi",
    # Discourse markers
    "mãrã",
    "ehei",
    "bre",
    "apoia",  # then
]

for particle in _particles:
    _exc[particle] = [{ORTH: particle}]

# Words with apostrophe (especially l' for palatalized l in some orthographies)
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
