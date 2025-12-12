

import itertools

from spacy.lang.char_classes import (
    ALPHA,
    ALPHA_LOWER,
    ALPHA_UPPER,
    CONCAT_QUOTES,
    CURRENCY,
    LIST_CURRENCY,
    LIST_ELLIPSES,
    LIST_ICONS,
    LIST_PUNCT,
    LIST_QUOTES,
    PUNCT,
)

_list_icons = [x for x in LIST_ICONS if x != "Â°"]
_list_icons = [x.replace("\\u00B0", "") for x in _list_icons]


_rup_variants = {
    "Ă": ["Ă", "ã", "A"],
    "Â": ["Â", "ã", "A"],
    "Î": ["Î", "ã", "I"],
    "Ș": ["Ș", "Ş", "S"],
    "Ț": ["Ț", "Ţ", "T"],
    "Ľ": ["Ľ", "L"],
    "Ń": ["Ń", "Ñ", "N"],
    "D̦": ["D̦", "D"],
}


def _make_rup_variants(tokens):
    """Generate orthographic variants for Aromanian tokens.
    
    Aromanian has multiple writing standards:
    - DIARO (Caragiu-Marioțeanu): ăâî/d̦/ľ/ń/ș/ț
    - Cunia (Tiberiu Cunia): ã/dz/lj/nj/sh/ts
    
    This function generates variants to handle both.
    """
    all_tokens = []
    for token in tokens:
        char_variants = []
        i = 0
        while i < len(token):
            char = token[i].upper()
            if char in _rup_variants:
                variants = _rup_variants[char]
                if token[i].islower():
                    variants = [v.lower() for v in variants]
                char_variants.append(variants)
            elif i + 1 < len(token):
                digraph = token[i:i+2].lower()
                if digraph == "sh":
                    char_variants.append([token[i:i+2], "ș", "ş"])
                    i += 1
                elif digraph == "ts":
                    char_variants.append([token[i:i+2], "ț", "ţ"])
                    i += 1
                elif digraph == "lj":
                    char_variants.append([token[i:i+2], "ľ", "l'"])
                    i += 1
                elif digraph == "nj":
                    char_variants.append([token[i:i+2], "ń", "ñ", "n'"])
                    i += 1
                elif digraph == "dz":
                    char_variants.append([token[i:i+2], "d̦"])
                    i += 1
                else:
                    char_variants.append([token[i]])
            else:
                char_variants.append([token[i]])
            i += 1
        
        for combo in itertools.product(*char_variants):
            all_tokens.append("".join(combo))
    
    return list(set(all_tokens))


_rup_prefixes = [
    "a-",
    "c-",
    "ca-",
    "cu-",
    "d-",
    "di-",
    "dintr-",
    "e-",
    "i-",
    "l-",
    "la-",
    "li-",
    "lu-",
    "m-",
    "mi-",
    "n-",
    "nã-",
    "ni-",
    "o-",
    "p-",
    "pã-",
    "pi-",
    "pitu-",
    "prit-",
    "pritu-",
    "s-",
    "se-",
    "si-",
    "ti-",
    "tra-",
    "tru-",
    "u-",
    "v-",
    "va-",
    "sh-",
    "shi-",
    "ș-",
    "și-",
    "ts-",
    "ț-",
]
_rup_prefix_variants = _make_rup_variants(_rup_prefixes)


_rup_suffixes = [
    "-a",
    "-lu",
    "-lji",
    "-le",
    "-lea",
    "-lor",
    "-lui",
    "-li",
    "-aestu",
    "-aestã",
    "-aesta",
    "-atsea",
    "-atsel",
    "-atselu",
    "-mi",
    "-mã",
    "-ti",
    "-lu",
    "-u",
    "-o",
    "-nã",
    "-vã",
    "-lji",
    "-li",
    "-lor",
    "-nju",
    "-ta",
    "-su",
    "-nostru",
    "-vostru",
    "-s",
    "-escu",
    "-i",
    "-sh",
    "-va",
    "-lea",
    "-a",
    "-sh",
    "-ts",
    "-lj",
    "-nj",
    "-ș",
    "-ț",
    "-ľ",
    "-ń",
]
_rup_suffix_variants = _make_rup_variants(_rup_suffixes)


_prefixes = (
    ["§", "%", "=", "—", "–", r"\+(?![0-9])"]
    + _rup_prefix_variants
    + LIST_PUNCT
    + LIST_ELLIPSES
    + LIST_QUOTES
    + LIST_CURRENCY
    + LIST_ICONS
)


_suffixes = (
    _rup_suffix_variants
    + LIST_PUNCT
    + LIST_ELLIPSES
    + LIST_QUOTES
    + _list_icons
    + ["'s", "'S", "'s", "'S"]
    + [
        r"(?<=[0-9])\+",
        r"(?<=°[FfCcKk])\.",
        r"(?<=[0-9])(?:{c})".format(c=CURRENCY),
        r"(?<=[0-9])(?:{u})".format(u="|".join(LIST_CURRENCY)),
        r"(?<=[0-9{al}{e}{q}])\.".format(
            al=ALPHA_LOWER,
            e=r"%²³",
            q=CONCAT_QUOTES,
        ),
    ]
)


_infixes = (
    LIST_ELLIPSES
    + _list_icons
    + [
        r"(?<=[0-9])[+\*^](?=[0-9-])",
        r"(?<=[{al}{q}])\.(?=[{au}{q}])".format(
            al=ALPHA_LOWER, au=ALPHA_UPPER, q=CONCAT_QUOTES
        ),
        r"(?<=[{a}]),(?=[{a}])".format(a=ALPHA),
        r"(?<=[{a}0-9])[:<>=](?=[{a}])".format(a=ALPHA),
        r"(?<=[{a}])'(?=[{a}])".format(a=ALPHA),
    ]
)

TOKENIZER_PREFIXES = _prefixes
TOKENIZER_SUFFIXES = _suffixes
TOKENIZER_INFIXES = _infixes

