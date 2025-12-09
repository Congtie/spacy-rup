# Lexical attributes for Aromanian
# Based on Romanian lex_attrs with Aromanian-specific patterns

from spacy.attrs import LIKE_NUM

# Aromanian number words
# Based on corpus analysis (senisioi/aromanian Tales dataset)
# Note: Aromanian uses both Latin-derived and some Greek-influenced numerals

_num_words = {
    # Cardinal numbers (Cunia orthography) - verified from corpus
    "un", "una", "unu", "unã",  # one (masc/fem)
    "doi", "doaua", "doauã", "dauã",  # two (masc/fem) - "doaua" is common in corpus
    "trei",  # three
    "patru",  # four
    "tsintsi",  # five
    "shase", "shasi",  # six
    "shapte", "shapti",  # seven
    "optu",  # eight
    "noaua", "noauã", "nauã",  # nine - "noaua" is in corpus
    "dzatsi", "dzatse",  # ten
    
    # Teens
    "unsprãdzatsi", "unsprãdzatse",
    "doisprãdzatsi", "doisprãdzatse",
    "treissprãdzatsi", "treissprãdzatse",
    "paisprãdzatsi", "paisprãdzatse",
    "tsintsisprãdzatsi", "tsintsisprãdzatse",
    "shasisprãdzatsi", "shasisprãdzatse",
    "shaptisprãdzatsi", "shaptisprãdzatse",
    "optusprãdzatsi", "optusprãdzatse",
    "nauãsprãdzatsi", "noauãsprãdzatse",
    
    # Tens (Greek-influenced for 20)
    "yinghits", "yinghitsi",  # twenty (from Greek ÎµÎ¯ÎºÎ¿ÏƒÎ¹)
    "treidzãts", "treidzãtsi",  # thirty
    "patrudzãts", "patrudzãtsi",  # forty
    "tsindzãts", "tsindzãtsi",  # fifty
    "shaidzãts", "shaidzãtsi",  # sixty
    "shaptidzãts", "shaptidzãtsi",  # seventy
    "optudzãts", "optudzãtsi",  # eighty
    "nauãdzãts", "noauãdzãtsi",  # ninety
    
    # Larger numbers
    "sutã", "suta", "sute",  # hundred - "suta" found in corpus
    "njilji", "njilju",  # thousand - found in corpus
    
    # DIARO orthography variants
    "dauă", "țintsi", "șase", "șapte", "năuă", "dzăț", "dzățe",
    "sută", "ńilji", "ńilju",
    
    # Ordinal numbers
    "protlu", "protã", "prota",  # first
    "doilea", "dauãlea", "doauãlea",  # second
    "treilea", "treia",  # third
    "patrulea", "patra",  # fourth
    "ultimu", "ultimã",  # last
}

# Fractions and special numbers
_num_words.update({
    "njiliunã", "miliunã",  # million (Cunia/DIARO)
    "giumãtati", "giumătate",  # half
    "sfãrtu", "sfărtu",  # quarter
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
    
    # Check for compound numbers like "dauã-dzatsi" (twenty-two)
    if "-" in text:
        parts = text.split("-")
        if all(p in _num_words for p in parts):
            return True
    
    return False


LEX_ATTRS = {
    LIKE_NUM: like_num,
}


