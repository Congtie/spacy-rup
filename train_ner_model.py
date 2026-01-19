import spacy
from spacy.util import minibatch, compounding
from spacy.training import Example
from spacy_rup import Aromanian
from pathlib import Path
import random
import json

def train_ner_model():
    data_path = Path("data/train.rup.ner.json")
    output_dir = Path("spacy_rup/resources/ner_model")
    
    if not data_path.exists():
        print(f"Error: Training data not found at {data_path}")
        return

    # Load data
    with open(data_path, "r", encoding="utf-8") as f:
        training_data = json.load(f)

    print(f"Loaded {len(training_data)} sentences for training.")

    # Initialize blank Aromanian model
    nlp = Aromanian()
    
    # Add NER pipe
    if "ner" not in nlp.pipe_names:
        ner = nlp.add_pipe("ner")
    else:
        ner = nlp.get_pipe("ner")

    # Add labels
    for _, annotations in training_data:
        for ent in annotations.get("entities", []):
            ner.add_label(ent[2])

    # Convert to Examples
    examples = []
    for text, annotations in training_data:
        try:
             predicted_doc = nlp.make_doc(text)
             example = Example.from_dict(predicted_doc, annotations)
             examples.append(example)
        except Exception as e:
             # print(f"Skipping sentence due to error: {e}")
             continue
    
    if not examples:
        print("No valid training examples found!")
        return
        
    # Initialize
    optimizer = nlp.initialize(lambda: examples)
    
    print(f"Training on {len(examples)} examples...")
    
    # Train
    try:
        for i in range(20): # 20 Epochs
            losses = {}  # Reset each epoch
            random.shuffle(examples)
            batches = minibatch(examples, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                nlp.update(batch, drop=0.35, losses=losses, sgd=optimizer)
            print(f"Epoch {i+1} Loss: {losses.get('ner', 0.0):.4f}")
    except KeyboardInterrupt:
        print("Training interrupted.")
    finally:
        # Save
        if not output_dir.exists():
            output_dir.mkdir(parents=True)
        
        nlp.to_disk(output_dir)
        print(f"Saved model to {output_dir}")

if __name__ == "__main__":
    train_ner_model()
