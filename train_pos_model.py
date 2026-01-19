import spacy
from spacy.util import minibatch, compounding
from spacy.training import Example
from spacy.tokens import Doc
from spacy_rup import Aromanian
from pathlib import Path
import random

def train_pos_model():
    data_path = Path("data/train.rup.conll")
    output_dir = Path("spacy_rup/resources/pos_model")
    
    if not data_path.exists():
        print(f"Error: Training data not found at {data_path}")
        return

    # Load data from CoNLL format (Word \t POS)
    train_data = []
    current_words = []
    current_tags = []
    
    with open(data_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                if current_words:
                    train_data.append((current_words, current_tags))
                    current_words = []
                    current_tags = []
                continue
            
            parts = line.split("\t")
            if len(parts) == 2:
                word = parts[0]
                tag = parts[1]
                current_words.append(word)
                # Convert '_' back to None for spaCy training
                current_tags.append(tag if tag != "_" else None)
                
    if current_words:
         train_data.append((current_words, current_tags))

    print(f"Loaded {len(train_data)} sentences for training.")

    # Initialize blank Aromanian model
    nlp = Aromanian()
    
    # Add tagger
    if "tagger" not in nlp.pipe_names:
        tagger = nlp.add_pipe("tagger")
    else:
        tagger = nlp.get_pipe("tagger")

    # Add labels
    for _, tags in train_data:
        for tag in tags:
            if tag: # Only add existing tags
                tagger.add_label(tag)

    # Convert to Examples
    examples = []
    for words, tags in train_data:
        # doc = Doc(nlp.vocab, words=list(words))
        # Use try-catch block for robust doc creation
        try:
             predicted_doc = Doc(nlp.vocab, words=list(words))
             reference_doc = Doc(nlp.vocab, words=list(words))
             for i, tag in enumerate(tags):
                 if tag is not None:
                     reference_doc[i].tag_ = tag
             example = Example(predicted_doc, reference_doc)
        except Exception as e:
             print(f"Skipping sentence due to error: {e}")
             continue
             
        examples.append(example)

    # Train
    # We may need to pass a valid example for initialization (one with tags)
    valid_examples = [e for e in examples if any(token.tag for token in e.reference)]
    
    if not valid_examples:
        print("No valid training examples found!")
        return
        
    optimizer = nlp.initialize(lambda: valid_examples)
    
    print(f"Training on {len(valid_examples)} examples...")
    losses = {}
    try:
        for i in range(10): # Reduced to 10 Epochs for speed
            random.shuffle(examples) # Use all examples for training context
            batches = minibatch(examples, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                nlp.update(batch, drop=0.5, losses=losses)
            print(f"Epoch {i+1} Loss: {losses.get('tagger', 0.0):.4f}")
    except KeyboardInterrupt:
        print("Training interrupted.")
    finally:
        # Save
        if not output_dir.exists():
            output_dir.mkdir(parents=True)
        
        nlp.to_disk(output_dir)
        print(f"Saved model to {output_dir}")

if __name__ == "__main__":
    train_pos_model()
