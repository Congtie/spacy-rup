# Aromanian language support for spaCy
# ISO 639-3 code: rup (Macedo-Romanian/Aromanian)
#
# Aromanian (armãneashti, armãnã, rrãmãneshti) is an Eastern Romance language
# spoken in the Balkans (Greece, Albania, North Macedonia, Romania, Bulgaria, Serbia).
#
# Note on orthography:
# There are multiple writing standards for Aromanian:
# - DIARO (Caragiu-Marioțeanu): ăâî/d̦/ľ/ń/ș/ț
# - Cunia (Tiberiu Cunia): ã/dz/lj/nj/sh/ts
# - Various other conventions in use
#
# This implementation uses a unified approach that can handle multiple orthographies.

from ...language import BaseDefaults, Language
from .lex_attrs import LEX_ATTRS
from .punctuation import TOKENIZER_INFIXES, TOKENIZER_PREFIXES, TOKENIZER_SUFFIXES
from .stop_words import STOP_WORDS
from .tokenizer_exceptions import TOKENIZER_EXCEPTIONS


class AromanianDefaults(BaseDefaults):
    tokenizer_exceptions = TOKENIZER_EXCEPTIONS
    prefixes = TOKENIZER_PREFIXES
    suffixes = TOKENIZER_SUFFIXES
    infixes = TOKENIZER_INFIXES
    lex_attr_getters = LEX_ATTRS
    stop_words = STOP_WORDS


class Aromanian(Language):
    lang = "rup"
    Defaults = AromanianDefaults


__all__ = ["Aromanian"]
