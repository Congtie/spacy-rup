# Stop words for Aromanian
# Based on analysis of the senisioi/aromanian corpus
# Includes both DIARO and Cunia orthographic variants
#
# Sources:
# - Frequency analysis of corpus.rup_cun and corpus.rup_std
# - Top ~200 most frequent function words
# - AroTranslate corpus (Tales dataset ~2000 sentences)

STOP_WORDS = set(
    """
a
aclo
aestu
aestã
aesta
aesti
al
anji
aoa
amu
ashi
ãshi
atsea
atsel
atumtsea
au
aua
avea

bun
bunã

ca
cã
că
cama
camu
cari
cãndu
cîndu
cându
cât
cãt
cît
cãte
cãtrã
cu
cum

da
deade
di
din
dit
ditu
dupã
după

ea
el
eali
elji
eli
eara
era
easte
easti
eu

fãrã
fărã
featse

ghine
ghini

hiu

i
ica
icã
iu
io
iar

la
li
lji
ľi
lo
ljea
ľea
lor
lu
lui

ma
mã
mari
mashi
mi
mine
multu
mini
mi
multu
mea
meu
mei
meali
njelu

nã
nă
nãs
nîs
nãsã
ni
ninga
nu
nostu
noastã
noi
nji
ńi

oarã
oară

pã
pãnã
pînă
pi
pri
pisti
pitu
poa
poati
prit
pritu
putu

s
s-
sã
să
si
sh
shi
și
ashi
sum
suntu
slu
snu

ti
tine
tora
trã
tră
tu
tra
tru
tse
țe
tsi
ți
tsiva
țiva
tutã
tută
tutu
tut
tuts

u
un
una
unu
un'
unã
ună
undã
undu

va
voi
vom
vã
vrea
vidzu

zã
"""
.split()
)

# Add variants with different orthographic standards
_cunia_variants = set()
_diaro_variants = set()

# Cunia uses: ã, dz, lj, nj, sh, ts
# DIARO uses: ă, â, î, d̦, ľ, ń, ș, ț

_orthography_map = {
    "ã": ["ă", "â", "î"],
    "sh": ["ș"],
    "ts": ["ț"],
    "lj": ["ľ", "l'"],
    "nj": ["ń", "ñ"],
    "dz": ["d̦"],
}

# Add common Romanian stop words that may appear in mixed texts
_romanian_common = [
    "și", "sau", "dar", "că", "de", "la", "în", "pe", "cu", "pentru",
    "este", "sunt", "era", "fost", "fi", "care", "ce", "nu", "da",
    "mai", "foarte", "doar", "acum", "așa", "astfel", "atunci",
    "când", "unde", "cum", "cât", "până", "prin", "spre", "între",
]

STOP_WORDS = STOP_WORDS.union(_romanian_common)  # type: ignore
