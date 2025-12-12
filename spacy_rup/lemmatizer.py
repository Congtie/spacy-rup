
from typing import Optional


VERB_LEMMAS = {
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
    "deadun": "dau",
    
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
    "putsãn": "potu",
    "putsãnã": "potu",
    "putsãnji": "potu",
    
    "yin": "yinu",
    "yinã": "yinu",
    "yinu": "yinu",
    "yine": "yinu",
    "yinje": "yinu",
    "yinea": "yinu",
    "yinjea": "yinu",
    "yinlu": "yinu",
    "yinyits": "yinu",
    "vinje": "yinu",
    "vine": "yinu",
    "vinea": "yinu",
    "vinishi": "yinu",
    "vinirã": "yinu",
    "vinjirã": "yinu",
    "vindu": "yinu",
    
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

NOUN_LEMMAS = {
    "ficiorlu": "ficior",
    "ficiorlji": "ficior",
    "caplu": "cap",
    "amirãlu": "amirã",
    "loclu": "loc",
    "hiljilu": "hilji",
    "aushlu": "aush",
    "picurarlu": "picurar",
    "araplu": "arap",
    "njiclu": "njic",
    "zborlu": "zbor",
    "vizirlu": "vizir",
    "foclu": "foc",
    "luplu": "lup",
    "mãratlu": "mãrat",
    "oarfãnlu": "oarfãn",
    "arãulu": "arãu",
    "perlu": "per",
    "neavutlu": "neavut",
    "cucotlu": "cucot",
    "capidanlu": "capidan",
    "vãshiljelu": "vãshilje",
    "tserlu": "tser",
    "dorlu": "dor",
    "bunlu": "bun",
    "thiriulu": "thiriu",
    "hãngilu": "hãngi",
    "cãnticlu": "cãntic",
    "maratlu": "marat",
    "chirolu": "chiro",
    
    "calea": "cale",
    "mintea": "minte",
    "lumea": "lume",
    "noaptea": "noapte",
    "mutrea": "mutre",
    "boatsea": "boatse",
    "muljearea": "muljare",
    "lamnjea": "lamnje",
    
    "ocljilji": "oclji",
    "pãrintsãlji": "pãrinte",
    "muntsãlji": "munte",
    "sotslji": "sots",
    "oaminjilji": "om",
    "cãnjilji": "cãne",
    "turtsãlji": "turcu",
    "gionjilji": "gione",
    "dratslji": "drac",
    "fratslji": "frate",
    "dintsãlji": "dinte",
    "oaspitslji": "oaspite",
    "picurarlji": "picurar",
    "ureclji": "ureaclje",
    "anghilji": "anghe",
    "armãnjilji": "armãn",
    
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


NOUN_ARTICLE_RULES = [
    ("lu", ""),
    ("rlu", "r"),
    
    ("a", "ã"),
    ("ea", "e"),
    
    ("lji", ""),
    ("nji", "n"),
    
    ("lui", ""),
    ("ului", ""),
    ("ãlji", "ã"),
    
    ("lji", ""),
    ("le", ""),
    ("lor", ""),
]

VERB_RULES = [
    ("irã", "", "past.3pl"),
    ("arã", "", "past.3pl"),
    ("urã", "", "past.3pl"),
    ("ãrã", "", "past.3pl"),
    
    ("ea", "", "impf.3sg"),
    ("eam", "", "impf.1sg"),
    ("eai", "", "impf.2sg"),
    ("eau", "", "impf.3pl"),
    
    ("ãndu", "", "ger"),
    ("indu", "", "ger"),
    
    ("ã", "", "subj.3sg"),
    
    ("are", "", "inf"),
    ("ire", "", "inf"),           
    ("ere", "", "inf"),
]

ADJ_RULES = [
    ("ã", "", "f.sg"),
    ("oasã", "os", "f.sg"),
    
    ("a", "", "f.sg.def"),
    
    ("i", "", "pl"),
    ("e", "", "f.pl"),
    ("shi", "s", "m.pl"),
]


def lemmatize_noun(word: str) -> str:
    """Lemmatize a noun by removing article suffixes."""
    word_lower = word.lower()
    
    if word_lower in NOUN_LEMMAS:
        return NOUN_LEMMAS[word_lower]
    
    for suffix, replacement in NOUN_ARTICLE_RULES:
        if word_lower.endswith(suffix) and len(word_lower) > len(suffix) + 1:
            return word_lower[:-len(suffix)] + replacement
    
    return word_lower


def lemmatize_verb(word: str) -> str:
    """Lemmatize a verb to its dictionary form."""
    word_lower = word.lower()
    
    if word_lower in VERB_LEMMAS:
        return VERB_LEMMAS[word_lower]
    
    for suffix, replacement, _ in VERB_RULES:
        if word_lower.endswith(suffix) and len(word_lower) > len(suffix) + 1:
            stem = word_lower[:-len(suffix)] + replacement
            return stem
    
    return word_lower


def lemmatize_adj(word: str) -> str:
    """Lemmatize an adjective to masculine singular."""
    word_lower = word.lower()
    
    if word_lower in ADJ_LEMMAS:
        return ADJ_LEMMAS[word_lower]
    
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
    
    if pos == "VERB":
        return lemmatize_verb(word)
    elif pos == "NOUN":
        return lemmatize_noun(word)
    elif pos == "ADJ":
        return lemmatize_adj(word)
    
    if word_lower in VERB_LEMMAS:
        return VERB_LEMMAS[word_lower]
    if word_lower in NOUN_LEMMAS:
        return NOUN_LEMMAS[word_lower]
    if word_lower in ADJ_LEMMAS:
        return ADJ_LEMMAS[word_lower]
    
    if word_lower.endswith(("lu", "a", "ea", "lji", "lor", "lui")):
        return lemmatize_noun(word)
    
    if word_lower.endswith(("irã", "arã", "urã", "ea", "ãndu")):
        return lemmatize_verb(word)
    
    return word_lower


if __name__ == "__main__":
    test_words = [
        ("ficiorlu", "NOUN"),
        ("caplu", "NOUN"),
        ("vulpea", "NOUN"),
        ("casa", "NOUN"),
        ("omlu", "NOUN"),
        
        ("featsirã", "VERB"),
        ("dzãse", "VERB"),
        ("avea", "VERB"),
        ("eara", "VERB"),
        
        ("bunã", "ADJ"),
        ("marea", "ADJ"),
        
        ("ficiorlu", None),
        ("dzãsirã", None),
    ]
    
    print("Aromanian Lemmatizer Test")
    print("=" * 50)
    
    for word, pos in test_words:
        lemma = lemmatize(word, pos)
        print(f"  {word:15} ({pos or 'auto':5}) -> {lemma}")
