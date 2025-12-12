

from spacy.language import Language
from spacy.tokens import Doc, Token

from .lemmatizer import lemmatize, VERB_LEMMAS, NOUN_LEMMAS, ADJ_LEMMAS

if not Token.has_extension('lemma_'):
    pass

@Language.factory(
    'aromanian_lemmatizer',
    assigns=['token.lemma'],
    default_config={'overwrite': False}
)
def create_aromanian_lemmatizer(nlp: Language, name: str, overwrite: bool):
    '''Create an Aromanian lemmatizer component.'''
    return AromanianLemmatizer(nlp, overwrite=overwrite)


class AromanianLemmatizer:
    '''
    Lemmatizer for Aromanian using lookup tables and suffix rules.
    
    This component assigns lemmas based on:
    1. Direct lookup in pre-defined tables (for common irregular forms)
    2. Suffix-based rules for regular morphology
    3. POS-informed lemmatization when POS tags are available
    '''
    
    def __init__(self, nlp: Language, overwrite: bool = False):
        self.nlp = nlp
        self.overwrite = overwrite
        self.name = 'aromanian_lemmatizer'
    
    def __call__(self, doc: Doc) -> Doc:
        '''Process a document, assigning lemmas to tokens.'''
        for token in doc:
            if token.lemma != 0 and not self.overwrite:
                continue
            
            pos = token.pos_ if token.pos_ else None
            lemma = lemmatize(token.text, pos)
            token.lemma_ = lemma
        
        return doc
    
    def to_disk(self, path, exclude=tuple()):
        pass
    
    def from_disk(self, path, exclude=tuple()):
        return self


def lemmatize_text(text: str, nlp=None) -> list:
    '''
    Lemmatize a text string and return list of (token, lemma) pairs.
    
    If nlp is not provided, creates a simple tokenizer.
    '''
    if nlp is None:
        import spacy
        nlp = spacy.blank('rup')
        nlp.add_pipe('aromanian_lemmatizer')
    
    doc = nlp(text)
    return [(token.text, token.lemma_) for token in doc]
