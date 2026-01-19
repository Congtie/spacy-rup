

import spacy
from spacy.language import Language
from spacy.lang.tokenizer_exceptions import BASE_EXCEPTIONS

from .lex_attrs import LEX_ATTRS
from .punctuation import TOKENIZER_INFIXES, TOKENIZER_PREFIXES, TOKENIZER_SUFFIXES
from .stop_words import STOP_WORDS
from .tokenizer_exceptions import TOKENIZER_EXCEPTIONS

from . import lemma_component



from .orthography import detect_orthography, cunia_to_diaro, diaro_to_cunia


class AromanianDefaults(Language.Defaults):
    tokenizer_exceptions = {**BASE_EXCEPTIONS, **TOKENIZER_EXCEPTIONS}
    prefixes = TOKENIZER_PREFIXES
    suffixes = TOKENIZER_SUFFIXES
    infixes = TOKENIZER_INFIXES
    lex_attr_getters = LEX_ATTRS
    stop_words = STOP_WORDS


@spacy.registry.languages("rup")
class Aromanian(Language):
    lang = 'rup'
    Defaults = AromanianDefaults


__all__ = ['Aromanian', 'detect_orthography', 'cunia_to_diaro', 'diaro_to_cunia']
