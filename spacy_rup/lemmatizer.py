# Lemmatizer for Aromanian
# Rule-based approach with lookup tables and suffix rules
# Based on forms extracted from the Aromanian corpus (Cunia orthography)

from typing import Optional

# ============================================================================
# LOOKUP TABLES - Forms extracted from corpus
# ============================================================================

# Verb forms -> infinitive (lemma)
VERB_LEMMAS = {
    # a hi (to be) - ~350 occurrences in corpus
    "hiu": "hiu",
    "eshti": "hiu",
    "easti": "hiu",
    "easte": "hiu",
    "him": "hiu",
    "hits": "hiu",
    "suntu": "hiu",
    "eara": "hiu",
    "fu": "hiu",
    "furã": "hiu",
    "fura": "hiu",
    
    # a avea (to have) - ~500+ occurrences
    "am": "am",
    "ai": "am",
    "are": "am",
    "avem": "am",
    "avets": "am",
    "au": "am",
    "avea": "am",
    "aveam": "am",
    "aveai": "am",
    "avu": "am",
    "avurã": "am",
    "avut": "am",
    "avutlu": "am",
    "aveaglje": "am",
    "avearea": "am",
    
    # a vrea (to want) - ~550+ occurrences
    "voi": "vrea",
    "vrea": "vrea",
    "vrei": "vrea",
    "va": "vrea",
    "vom": "vrea",
    "vrem": "vrea",
    "vrets": "vrea",
    "vor": "vrea",
    "vream": "vrea",
    "vreai": "vrea",
    "vreau": "vrea",
    "vrurã": "vrea",
    "vreare": "vrea",
    "vrearea": "vrea",
    "vreun": "vrea",
    "vreava": "vrea",
    "vreavã": "vrea",
    
    # a dzãtse (to say) - ~200+ occurrences
    "dzãc": "dzãc",
    "dzãcã": "dzãc",
    "dzãts": "dzãc",
    "dzãtse": "dzãc",
    "dzãtsi": "dzãc",
    "dzãtsem": "dzãc",
    "dzãtsets": "dzãc",
    "dzãtsea": "dzãc",
    "dzãtseai": "dzãc",
    "dzãtseam": "dzãc",
    "dzãtseare": "dzãc",
    "dzatse": "dzãc",
    "dzatsi": "dzãc",
    "dzatsile": "dzãc",
    "dzãca": "dzãc",
    
    # a fac (to do/make) - ~400+ occurrences
    "fac": "fac",
    "facã": "fac",
    "fats": "fac",
    "fatsã": "fac",
    "fatse": "fac",
    "fatsi": "fac",
    "fatsa": "fac",
    "fatsire": "fac",
    "fatsem": "fac",
    "fãtsea": "fac",
    "featse": "fac",
    "featsirã": "fac",
    "featsim": "fac",
    "featsishi": "fac",
    "disfats": "fac",
    "disfeatse": "fac",
    
    # a da (to give) - ~190+ occurrences
    "dau": "dau",
    "dai": "dau",
    "da": "dau",
    "dam": "dau",
    "dats": "dau",
    "deade": "dau",
    "deadi": "dau",
    "deadim": "dau",
    "deadeshi": "dau",
    "deadishi": "dau",
    "deadirã": "dau",
    "deadun": "dau",  # împreună
    
    # a shtiu (to know) - ~180+ occurrences
    "shtiu": "shtiu",
    "shtii": "shtiu",
    "shtie": "shtiu",
    "shti": "shtiu",
    "shtim": "shtiu",
    "shtits": "shtiu",
    "shtia": "shtiu",
    "shtiam": "shtiu",
    "shtiai": "shtiu",
    "shtibã": "shtiu",
    "shtire": "shtiu",
    "shtirea": "shtiu",
    "shtiri": "shtiu",
    "shtiindalui": "shtiu",
    
    # a potu (can) - ~200+ occurrences
    "pot": "potu",
    "pots": "potu",
    "poate": "potu",
    "puts": "potu",
    "putsã": "potu",
    "putem": "potu",
    "putes": "potu",
    "putea": "potu",
    "puteam": "potu",
    "putu": "potu",
    "putui": "potu",
    "puturã": "potu",
    "putut": "potu",
    "puteare": "potu",
    "putsãn": "potu",  # puțin
    "putsãnã": "potu",
    "putsãnji": "potu",
    
    # a yini (to come) - ~300+ occurrences
    "yin": "yinu",
    "yinã": "yinu",
    "yinu": "yinu",
    "yine": "yinu",
    "yinje": "yinu",
    "yinea": "yinu",
    "yinjea": "yinu",
    "yinlu": "yinu",
    "yinyits": "yinu",
    # cu v- initial (variante)
    "vinje": "yinu",
    "vine": "yinu",
    "vinea": "yinu",
    "vinishi": "yinu",
    "vinirã": "yinu",
    "vinjirã": "yinu",
    "vindu": "yinu",
    
    # a vedu (to see) - ~290+ occurrences
    "vedu": "vedu",
    "vedz": "vedu",
    "vedzi": "vedu",
    "veade": "vedu",
    "veadã": "vedu",
    "videam": "vedu",
    "vidzu": "vedu",
    "vidzui": "vedu",
    "vidzurã": "vedu",
    "vidzushi": "vedu",
    "vidzi": "vedu",
    "vidzut": "vedu",
    "vidzutã": "vedu",
    "vidzute": "vedu",
    "vidui": "vedu",
    "veduiã": "vedu",
    "vidzãndalui": "vedu",
    
    # a ljau (to take) - ~100+ occurrences (excluding "lji" pronoun)
    "ljau": "ljau",
    "ljei": "ljau",
    "lja": "ljau",
    "ljam": "ljau",
    "ljea": "ljau",
    "ljeai": "ljau",
    "ljeau": "ljau",
    "ljia": "ljau",
    "lo": "ljau",
    "loarã": "ljau",
    
    # a ducu (to go/carry) - ~130+ occurrences
    "duc": "ducu",
    "duca": "ducu",
    "ducã": "ducu",
    "ducu": "ducu",
    "duts": "ducu",
    "dutse": "ducu",
    "dutsets": "ducu",
    "dutsea": "ducu",
    "dutseam": "ducu",
    "dutsem": "ducu",
    "duchea": "ducu",
    "ducheascã": "ducu",
    "duchescu": "ducu",
    "duchii": "ducu",
    "duchirã": "ducu",
}

# Noun forms -> lemma (without article)
# Based on corpus frequency analysis
NOUN_LEMMAS = {
    # Masculine nouns with definite article -lu
    "ficiorlu": "ficior",     # boy (140)
    "ficiorlji": "ficior",    # boys (27)
    "caplu": "cap",           # head (85)
    "amirãlu": "amirã",       # emperor (69)
    "loclu": "loc",           # place (50)
    "hiljilu": "hilji",       # son (39)
    "aushlu": "aush",         # old man (32)
    "picurarlu": "picurar",   # shepherd (32)
    "araplu": "arap",         # black man (25)
    "njiclu": "njic",         # small one (24)
    "zborlu": "zbor",         # word (22)
    "vizirlu": "vizir",       # vizier (21)
    "foclu": "foc",           # fire (20)
    "luplu": "lup",           # wolf (19)
    "mãratlu": "mãrat",       # poor man (18)
    "oarfãnlu": "oarfãn",     # orphan (17)
    "arãulu": "arãu",         # bad one (14)
    "perlu": "per",           # hair (14)
    "neavutlu": "neavut",     # poor (14)
    "cucotlu": "cucot",       # rooster (14)
    "capidanlu": "capidan",   # captain (14)
    "vãshiljelu": "vãshilje", # king (13)
    "tserlu": "tser",         # sky (13)
    "dorlu": "dor",           # longing (13)
    "bunlu": "bun",           # good one (12)
    "thiriulu": "thiriu",     # beast (11)
    "hãngilu": "hãngi",       # inn (10)
    "cãnticlu": "cãntic",     # song (10)
    "maratlu": "marat",       # poor (10)
    "chirolu": "chiro",       # time (10)
    
    # Feminine nouns with article -ea
    "calea": "cale",          # way (74)
    "mintea": "minte",        # mind (59)
    "lumea": "lume",          # world (51)
    "noaptea": "noapte",      # night (40)
    "mutrea": "mutre",        # face (34)
    "boatsea": "boatse",      # voice (20)
    "muljearea": "muljare",   # woman (18)
    "lamnjea": "lamnje",      # blade (18)
    
    # Plural with -lji (genitive/dative)
    "ocljilji": "oclji",      # eyes (76)
    "pãrintsãlji": "pãrinte", # parents (20)
    "muntsãlji": "munte",     # mountains (16)
    "sotslji": "sots",        # companions (15)
    "oaminjilji": "om",       # people (14)
    "cãnjilji": "cãne",       # dogs (13)
    "turtsãlji": "turcu",     # Turks (12)
    "gionjilji": "gione",     # brave ones (11)
    "dratslji": "drac",       # devils (9)
    "fratslji": "frate",      # brothers (9)
    "dintsãlji": "dinte",     # teeth (9)
    "oaspitslji": "oaspite",  # guests (8)
    "picurarlji": "picurar",  # shepherds (6)
    "ureclji": "ureaclje",    # ears (6)
    "anghilji": "anghe",      # angels (6)
    "armãnjilji": "armãn",    # Aromanians (6)
    
    # Common nouns - additional
    "omlu": "om",
    "omului": "om",
    "oaminji": "om",
    "oaminjlor": "om",
    "feata": "featã",
    "featãlji": "featã",
    "feate": "featã",
    "casa": "casã",
    "casãlji": "casã",
    "case": "casã",
    "vulpea": "vulpe",
    "vulpãlji": "vulpe",
    "vulpi": "vulpe",
}

# Adjective forms -> masculine singular
ADJ_LEMMAS = {
    "buna": "bun",
    "bunã": "bun",
    "bunlji": "bun",
    "bunã": "bun",
    
    "marea": "mare",
    "mari": "mare",
    "marli": "mare",
    
    "frumoslu": "frumos",
    "frumoasa": "frumos",
    "frumoshi": "frumos",
    
    "njiclu": "njic",
    "njica": "njic",
    "njits": "njic",
}

# ============================================================================
# SUFFIX RULES - For regular morphology
# ============================================================================

# Noun article removal rules: (suffix_to_remove, suffix_to_add)
NOUN_ARTICLE_RULES = [
    # Masculine singular definite article
    ("lu", ""),      # ficiorlu -> ficior, caplu -> cap
    ("rlu", "r"),    # picurarlu -> picurar (keeps the r)
    
    # Feminine singular definite article  
    ("a", "ã"),      # casa -> casã, feata -> featã
    ("ea", "e"),     # vulpea -> vulpe, mintea -> minte
    
    # Masculine plural
    ("lji", ""),     # ficiorlji -> ficior (approximately)
    ("nji", "n"),    # oaminji -> oamin -> om
    
    # Genitive/Dative
    ("lui", ""),     # ficiorului -> ficior
    ("ului", ""),    # omului -> om
    ("ãlji", "ã"),   # casãlji -> casã
    
    # Plural definite
    ("lji", ""),     # ocljilji -> oclji
    ("le", ""),      # casele -> case
    ("lor", ""),     # caslor -> cas
]

# Verb conjugation rules: (ending, base_ending, tense_info)
VERB_RULES = [
    # Perfect simplu (past simple)
    ("irã", "", "past.3pl"),      # featsirã -> feats (approximately)
    ("arã", "", "past.3pl"),      # loarã -> lo, bãgarã -> bãg
    ("urã", "", "past.3pl"),      # vidzurã -> vidz
    ("ãrã", "", "past.3pl"),      # dzãsirã -> dzãs
    
    # Imperfect
    ("ea", "", "impf.3sg"),       # dzãtsea -> dzãts, fãtsea -> fãts
    ("eam", "", "impf.1sg"),      # fãtseam -> fãts
    ("eai", "", "impf.2sg"),
    ("eau", "", "impf.3pl"),
    
    # Present participle / Gerund
    ("ãndu", "", "ger"),          # fãtsãndu -> fãts
    ("indu", "", "ger"),          # vidzindu -> vidz
    
    # Subjunctive (often same as infinitive stem)
    ("ã", "", "subj.3sg"),        # s-facã -> fac, s-hibã -> hib
    
    # Infinitive lung (long infinitive as noun)
    ("are", "", "inf"),           # fãtseare -> fãts (doing)
    ("ire", "", "inf"),           
    ("ere", "", "inf"),
]

# Adjective agreement rules
ADJ_RULES = [
    # Feminine singular
    ("ã", "", "f.sg"),            # bunã -> bun, albã -> alb
    ("oasã", "os", "f.sg"),       # frumoasã -> frumos
    
    # Feminine with article
    ("a", "", "f.sg.def"),        # buna -> bun, marea -> mar (not perfect)
    
    # Plural
    ("i", "", "pl"),              # buni -> bun, mari -> mar
    ("e", "", "f.pl"),            # bune -> bun
    ("shi", "s", "m.pl"),         # frumoshi -> frumos
]


def lemmatize_noun(word: str) -> str:
    """Lemmatize a noun by removing article suffixes."""
    word_lower = word.lower()
    
    # Check lookup first
    if word_lower in NOUN_LEMMAS:
        return NOUN_LEMMAS[word_lower]
    
    # Apply suffix rules
    for suffix, replacement in NOUN_ARTICLE_RULES:
        if word_lower.endswith(suffix) and len(word_lower) > len(suffix) + 1:
            return word_lower[:-len(suffix)] + replacement
    
    return word_lower


def lemmatize_verb(word: str) -> str:
    """Lemmatize a verb to its dictionary form."""
    word_lower = word.lower()
    
    # Check lookup first
    if word_lower in VERB_LEMMAS:
        return VERB_LEMMAS[word_lower]
    
    # Apply suffix rules
    for suffix, replacement, _ in VERB_RULES:
        if word_lower.endswith(suffix) and len(word_lower) > len(suffix) + 1:
            stem = word_lower[:-len(suffix)] + replacement
            # Try to find a known verb with this stem
            return stem
    
    return word_lower


def lemmatize_adj(word: str) -> str:
    """Lemmatize an adjective to masculine singular."""
    word_lower = word.lower()
    
    # Check lookup first
    if word_lower in ADJ_LEMMAS:
        return ADJ_LEMMAS[word_lower]
    
    # Apply suffix rules
    for suffix, replacement, _ in ADJ_RULES:
        if word_lower.endswith(suffix) and len(word_lower) > len(suffix) + 1:
            return word_lower[:-len(suffix)] + replacement
    
    return word_lower


def lemmatize(word: str, pos: Optional[str] = None) -> str:
    """
    Lemmatize an Aromanian word.
    
    Args:
        word: The word to lemmatize
        pos: Part of speech tag (NOUN, VERB, ADJ, etc.) - optional
        
    Returns:
        The lemma (base form) of the word
    """
    if not word:
        return word
    
    word_lower = word.lower()
    
    # If POS is known, use specific lemmatizer
    if pos == "VERB":
        return lemmatize_verb(word)
    elif pos == "NOUN":
        return lemmatize_noun(word)
    elif pos == "ADJ":
        return lemmatize_adj(word)
    
    # Without POS, try all lookups first
    if word_lower in VERB_LEMMAS:
        return VERB_LEMMAS[word_lower]
    if word_lower in NOUN_LEMMAS:
        return NOUN_LEMMAS[word_lower]
    if word_lower in ADJ_LEMMAS:
        return ADJ_LEMMAS[word_lower]
    
    # Heuristic: try noun rules (most common)
    # Check for common noun article patterns
    if word_lower.endswith(("lu", "a", "ea", "lji", "lor", "lui")):
        return lemmatize_noun(word)
    
    # Check for verb patterns
    if word_lower.endswith(("irã", "arã", "urã", "ea", "ãndu")):
        return lemmatize_verb(word)
    
    return word_lower


# For testing
if __name__ == "__main__":
    test_words = [
        # Nouns with article
        ("ficiorlu", "NOUN"),
        ("caplu", "NOUN"),
        ("vulpea", "NOUN"),
        ("casa", "NOUN"),
        ("omlu", "NOUN"),
        
        # Verbs
        ("featsirã", "VERB"),
        ("dzãse", "VERB"),
        ("avea", "VERB"),
        ("eara", "VERB"),
        
        # Adjectives
        ("bunã", "ADJ"),
        ("marea", "ADJ"),
        
        # Without POS
        ("ficiorlu", None),
        ("dzãsirã", None),
    ]
    
    print("Aromanian Lemmatizer Test")
    print("=" * 50)
    
    for word, pos in test_words:
        lemma = lemmatize(word, pos)
        print(f"  {word:15} ({pos or 'auto':5}) -> {lemma}")
