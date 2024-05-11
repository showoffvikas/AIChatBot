import spacy
import yaml
import os
import random

def train_model(output_dir, yaml_files):
    nlp = spacy.blank("en")
    textcat = nlp.add_pipe("textcat_multilabel")

    labels = set()

    for yaml_file in yaml_files:
        with open(yaml_file, 'r') as file:
            yaml_data = yaml.safe_load(file)

        categories = yaml_data.get("categories", [])
        for category in categories:
            labels.add(category)

    for label in labels:
        textcat.add_label(label)

    optimizer = nlp.begin_training()

    # Training data
    train_data = []

    for yaml_file in yaml_files:
        with open(yaml_file, 'r') as file:
            yaml_data = yaml.safe_load(file)

        categories = yaml_data.get("categories", [])
        conversations = yaml_data.get("conversations", [])
        for conversation in conversations:
            question = conversation[0]
            answers = conversation[1:]
            for answer in answers:
                for category in categories:
                    train_data.append((question, {"cats": {category: 1}}))
                    train_data.append((answer, {"cats": {category: 0}}))

    for epoch in range(10):
        losses = {}
        random.shuffle(train_data)
        batches = spacy.util.minibatch(train_data, size=spacy.util.compounding(4.0, 32.0, 1.001))
        for batch in batches:
            texts, annotations = zip(*batch)
            example = [spacy.training.Example.from_dict(nlp.make_doc(text), annotation) for text, annotation in zip(texts, annotations)]
            nlp.update(example, sgd=optimizer, losses=losses)
        print("Epoch:", epoch, "Losses:", losses)

  
    nlp.to_disk(output_dir)
    print("Trained model saved to:", output_dir)

if __name__ == '__main__':
   
    directory = "C:/Users/acer/Desktop/New folder/data"
    yaml_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith(".yml")]

    
    train_model("C:/Users/acer/Desktop/New folder/model", yaml_files)
