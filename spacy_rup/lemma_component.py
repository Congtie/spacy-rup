# Aromanian Lemmatizer component for spaCy
# Based on lookup tables and suffix rules

from spacy.language import Language
from spacy.tokens import Doc, Token

from .lemmatizer import lemmatize, VERB_LEMMAS, NOUN_LEMMAS, ADJ_LEMMAS

# Register the lemma extension if not already registered
if not Token.has_extension('lemma_'):
    pass  # lemma_ is already a built-in attribute

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
            # Skip if lemma already set and not overwriting
            if token.lemma != 0 and not self.overwrite:
                continue
            
            # Get lemma based on POS if available
            pos = token.pos_ if token.pos_ else None
            lemma = lemmatize(token.text, pos)
            token.lemma_ = lemma
        
        return doc
    
    def to_disk(self, path, exclude=tuple()):
        pass
    
    def from_disk(self, path, exclude=tuple()):
        return self


# Convenience function for standalone lemmatization
def lemmatize_text(text: str, nlp=None) -> list:
    '''
    Lemmatize a text string and return list of (token, lemma) pairs.
    
    If nlp is not provided, creates a simple tokenizer.
    '''
    if nlp is None:
        # Create minimal pipeline
        import spacy
        nlp = spacy.blank('rup')
        nlp.add_pipe('aromanian_lemmatizer')
    
    doc = nlp(text)
    return [(token.text, token.lemma_) for token in doc]
