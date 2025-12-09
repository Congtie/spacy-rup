# Lexical attributes for Aromanian
# Based on Romanian lex_attrs with Aromanian-specific patterns

from spacy.attrs import LIKE_NUM

# Aromanian number words
# Based on corpus analysis (senisioi/aromanian Tales dataset)
# Note: Aromanian uses both Latin-derived and some Greek-influenced numerals

_num_words = {
    # Cardinal numbers (Cunia orthography) - verified from corpus
    "un", "una", "unu", "unÃ£",  # one (masc/fem)
    "doi", "doauÃ£", "dauÃ£",  # two (masc/fem) - "doauÃ£" is common in corpus
    "trei",  # three
    "patru",  # four
    "tsintsi",  # five
    "shase", "shasi",  # six
    "shapte", "shapti",  # seven
    "optu",  # eight
    "noauÃ£", "nauÃ£",  # nine - "noauÃ£" is in corpus
    "dzatsi", "dzatse",  # ten
    
    # Teens
    "unsprÃ£dzatsi", "unsprÃ£dzatse",
    "doisprÃ£dzatsi", "doisprÃ£dzatse",
    "treissprÃ£dzatsi", "treissprÃ£dzatse",
    "paisprÃ£dzatsi", "paisprÃ£dzatse",
    "tsintsisprÃ£dzatsi", "tsintsisprÃ£dzatse",
    "shasisprÃ£dzatsi", "shasisprÃ£dzatse",
    "shaptisprÃ£dzatsi", "shaptisprÃ£dzatse",
    "optusprÃ£dzatsi", "optusprÃ£dzatse",
    "nauÃ£sprÃ£dzatsi", "noauÃ£sprÃ£dzatse",
    
    # Tens (Greek-influenced for 20)
    "yinghits", "yinghitsi",  # twenty (from Greek ÎµÎ¯ÎºÎ¿ÏƒÎ¹)
    "treidzÃ£ts", "treidzÃ£tsi",  # thirty
    "patrudzÃ£ts", "patrudzÃ£tsi",  # forty
    "tsindzÃ£ts", "tsindzÃ£tsi",  # fifty
    "shaidzÃ£ts", "shaidzÃ£tsi",  # sixty
    "shaptidzÃ£ts", "shaptidzÃ£tsi",  # seventy
    "optudzÃ£ts", "optudzÃ£tsi",  # eighty
    "nauÃ£dzÃ£ts", "noauÃ£dzÃ£tsi",  # ninety
    
    # Larger numbers
    "sutÃ£", "suta", "sute",  # hundred - "suta" found in corpus
    "njilji", "njilju",  # thousand - found in corpus
    
    # DIARO orthography variants
    "dauÄƒ", "È›intsi", "È™ase", "È™apte", "nÄƒuÄƒ", "dzÄƒÈ›", "dzÄƒÈ›e",
    "sutÄƒ", "Å„ilji", "Å„ilju",
    
    # Ordinal numbers
    "protlu", "protÃ£", "prota",  # first
    "doilea", "dauÃ£lea", "doauÃ£lea",  # second
    "treilea", "treia",  # third
    "patrulea", "patra",  # fourth
    "ultimu", "ultimÃ£",  # last
}

# Fractions and special numbers
_num_words.update({
    "njiliunÃ£", "miliunÃ£",  # million (Cunia/DIARO)
    "giumÃ£tati", "giumÄƒtate",  # half
    "sfÃ£rtu", "sfÄƒrtu",  # quarter
    "zero", "zeru",
})


def like_num(text):
    """Check if text represents a number in Aromanian."""
    # Clean and normalize
    text = text.lower().replace(",", "").replace(".", "")
    
    # Check if it's a digit
    if text.isdigit():
        return True
    
    # Check if it looks like a number with decimal
    if text.count(",") == 1 or text.count(".") == 1:
        parts = text.replace(",", ".").split(".")
        if all(p.isdigit() for p in parts if p):
            return True
    
    # Check word numbers
    if text in _num_words:
        return True
    
    # Check for compound numbers like "dauÃ£-dzatsi" (twenty-two)
    if "-" in text:
        parts = text.split("-")
        if all(p in _num_words for p in parts):
            return True
    
    return False


LEX_ATTRS = {
    LIKE_NUM: like_num,
}


