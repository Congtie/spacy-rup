

from spacy.attrs import LIKE_NUM


_num_words = {
    "un", "una", "unu", "unã",
    "doi", "doaua", "doauã", "dauã",
    "trei",
    "patru",
    "tsintsi",
    "shase", "shasi",
    "shapte", "shapti",
    "optu",
    "noaua", "noauã", "nauã",
    "dzatsi", "dzatse",
    
    "unsprãdzatsi", "unsprãdzatse",
    "doisprãdzatsi", "doisprãdzatse",
    "treissprãdzatsi", "treissprãdzatse",
    "paisprãdzatsi", "paisprãdzatse",
    "tsintsisprãdzatsi", "tsintsisprãdzatse",
    "shasisprãdzatsi", "shasisprãdzatse",
    "shaptisprãdzatsi", "shaptisprãdzatse",
    "optusprãdzatsi", "optusprãdzatse",
    "nauãsprãdzatsi", "noauãsprãdzatse",
    
    "yinghits", "yinghitsi",
    "treidzãts", "treidzãtsi",
    "patrudzãts", "patrudzãtsi",
    "tsindzãts", "tsindzãtsi",
    "shaidzãts", "shaidzãtsi",
    "shaptidzãts", "shaptidzãtsi",
    "optudzãts", "optudzãtsi",
    "nauãdzãts", "noauãdzãtsi",
    
    "sutã", "suta", "sute",
    "njilji", "njilju",
    
    "dauă", "țintsi", "șase", "șapte", "năuă", "dzăț", "dzățe",
    "sută", "ńilji", "ńilju",
    
    "protlu", "protã", "prota",
    "doilea", "dauãlea", "doauãlea",
    "treilea", "treia",
    "patrulea", "patra",
    "ultimu", "ultimã",
}

_num_words.update({
    "njiliunã", "miliunã",
    "giumãtati", "giumătate",
    "sfãrtu", "sfărtu",
    "zero", "zeru",
})


def like_num(text):
    """Check if text represents a number in Aromanian."""
    text = text.lower().replace(",", "").replace(".", "")
    
    if text.isdigit():
        return True
    
    if text.count(",") == 1 or text.count(".") == 1:
        parts = text.replace(",", ".").split(".")
        if all(p.isdigit() for p in parts if p):
            return True
    
    if text in _num_words:
        return True
    
    if "-" in text:
        parts = text.split("-")
        if all(p in _num_words for p in parts):
            return True
    
    return False


LEX_ATTRS = {
    LIKE_NUM: like_num,
}


