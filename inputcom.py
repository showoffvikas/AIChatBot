import os
import sys
import spacy
import yaml
import random

def get_most_similar_question(nlp, question):
    directory = "C:/Users/acer/Desktop/New folder/data"
    yaml_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith(".yml")]
    nlp = spacy.load("C:/Users/acer/Desktop/New folder/model")    
    similarity_scores = {}
    
    # Calculate similarity scores for each category
    for yaml_file in yaml_files:
        with open(yaml_file, 'r') as file:
            yaml_data = yaml.safe_load(file)
        
        categories = yaml_data.get("categories", [])
        for category in categories:
            conversations = yaml_data.get("conversations", [])
            for conversation in conversations:
                conversation_question = conversation[0]
                similarity = nlp(question).similarity(nlp(conversation_question))
                similarity_scores[conversation_question] = similarity
    
    # Sort similarity scores in descending order
    sorted_scores = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Print the most similar question and its corresponding answer
    if sorted_scores:
        most_similar_question, _ = sorted_scores[0]
        print("Most Similar Question:", most_similar_question)
        
        # Retrieve and print the corresponding answer from the YAML files
        for yaml_file in yaml_files:
            with open(yaml_file, 'r') as file:
                yaml_data = yaml.safe_load(file)

            categories = yaml_data.get("categories", [])
            for category in categories:
                conversations = yaml_data.get("conversations", [])
                for conversation in conversations:
                    conversation_question = conversation[0]
                    if conversation_question == most_similar_question:
                        conversation_answers = conversation[1:]
                        print("Answer(s):")
                        for answer in conversation_answers:
                            print("Answer(s):",answer)
                            return answer
    
    # If no similar question found
    print("No similar question found.")


